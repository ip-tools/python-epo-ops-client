# -*- coding: utf-8 -*-
import logging
import warnings
from base64 import b64encode
from typing import List, Optional, Union
from xml.etree import ElementTree as ET

import requests
from requests.exceptions import HTTPError

from . import exceptions
from .middlewares import Throttler
from .models import (
    NETWORK_TIMEOUT,
    AccessToken,
    Docdb,
    Epodoc,
    Original,
    Request,
)

log = logging.getLogger(__name__)


class Client(object):
    __auth_url__ = "https://ops.epo.org/3.2/auth/accesstoken"
    __service_url_prefix__ = "https://ops.epo.org/3.2/rest-services"

    __family_path__ = "family"
    __images_path__ = "published-data/images"
    __number_path__ = "number-service"
    __published_data_path__ = "published-data"
    __published_data_search_path__ = "published-data/search"
    __register_path__ = "register"
    __register_search_path__ = "register/search"

    def __init__(self, key, secret, accept_type="xml", middlewares=None):
        self.accept_type = "application/{0}".format(accept_type)
        self.middlewares = middlewares
        if middlewares is None:
            self.middlewares = [Throttler()]
        self.request = Request(self.middlewares)
        self.key = key
        self.secret = secret
        self._access_token = None

    def family(
        self,
        reference_type: str,
        input: Union[Docdb, Epodoc],
        endpoint=None,
        constituents: Optional[List[str]] = None,
    ) -> requests.Response:
        """
        Retrieves the patent numbers of the extended patent family related to the input (INPADOC family).

        Args:
            reference_type (str): Any of "publication", "application", or "priority".
            input (Epodoc or Docdb): The document number. Cannot be Original.
            endpoint (optional): None. Not applicable for family service.
            constituents (List[str], optional): List of "biblio", "legal" or both.
                                                Defaults to None.

        Returns:
            requests.Response: a requests.Response object.

        Examples:
            >>> response = client.family("publication", epo_ops.models.Epodoc("EP1000000"))
            >>> response
            <Response [200]>
            >>> len(response.text)
            8790

            >>> response_with_constituents = client.family("publication", epo_ops.models.Epodoc("EP1000000"), None, ["biblio", "legal"])
            >>> response_with_constituents
            <Response [200]>
            >>> len(response_with_constituents.text)
            160206
        """
        if endpoint is not None:
            warnings.warn(
                "The `endpoint` argument is not used in this context and will be removed.",
                DeprecationWarning,
                stacklevel=2,
            )

        url = self._make_request_url(
            dict(
                service=self.__family_path__,
                reference_type=reference_type,
                input=input,
                endpoint=None,
                constituents=constituents,
                use_get=True,
            )
        )
        return self._make_request(url, None, params=input.as_api_input(), use_get=True)

    def image(
        self, path: str, range: int = 1, document_format: str = "application/tiff"
    ) -> requests.Response:
        """
        Retrieve the image page for a given path, one page at a time.
        The path needs to be retrieved from the xml resulting from a prior inquiry using
        the published_data() service with the endpoint='images'.
        """
        return self._image_request(path, range, document_format)

    def number(
        self,
        reference_type: str,
        input: Union[Original, Docdb, Epodoc],
        output_format: Union[Original, Docdb, Epodoc],
    ) -> requests.Response:
        """
        This service converts a patent number from one input format into another format.

        Use-cases: Given that other OPS services use only the Epodoc or Docdb format,
        the general use-case of this method would be to convert the Original format
        into either the Docdb or the Epodoc format.

        Note: It is especially important to include the date in number requests whenever
        possible because number formatting may vary depending on the date.
        """
        possible_conversions = {
            "docdb": ["original", "epodoc"],
            "epodoc": ["original"],
            "original": ["docdb", "epodoc"],
        }
        input_format = input.__class__.__name__.lower()

        if output_format not in possible_conversions[input_format]:
            raise exceptions.InvalidNumberConversion(
                "Cannot convert from {0} to {1}".format(input_format, output_format)
            )
        return self._service_request(
            dict(
                service=self.__number_path__,
                reference_type=reference_type,
                input=input,
                endpoint=output_format,
            )
        )

    def published_data(
        self,
        reference_type: str,
        input: Union[Docdb, Epodoc],
        endpoint="biblio",
        constituents: Optional[List[str]] = None,
    ) -> requests.Response:
        """
        Retrieval service for published data.

        Args:
            reference_type (str): Any of "publication", "application", or "priority".
            input (Epodoc or Docdb): The document number as a Epodoc or Docdb data object.
            endpoint (str, optional): "biblio", "equivalents", "abstract", "claims", "description",
                                      "fulltext", "images". Defaults to "biblio".
            constituents (list[str], optional): List of "biblio", "abstract", "images", "full cycle".

        Returns:
            requests.Response: a requests.Response object

        Note:
        1) input cannot be a models.Original
        2) only the endpoint "biblio" or "equivalents" use the constituents parameter.
        3) the images and fulltext retrieval require a two-step process: inquiry, then retrieval, e.g.
           - client.published_data(..., endpoint='images',...) to retrieve the image path, then
           - client.image(path=...)
        """
        return self._service_request(
            dict(
                service=self.__published_data_path__,
                reference_type=reference_type,
                input=input,
                endpoint=endpoint,
                constituents=constituents,
            )
        )

    def published_data_search(
        self,
        cql: str,
        range_begin: int = 1,
        range_end: int = 25,
        constituents: Optional[List[str]] = None,
    ) -> requests.Response:
        """
        Performs a bibliographic search ussing common query language (CQL) to retrieve the data.
        Possible constituents: "abstract", "biblio" and/or "full-cycle".
        """
        range = dict(key="X-OPS-Range", begin=range_begin, end=range_end)
        return self._search_request(
            dict(
                service=self.__published_data_search_path__, constituents=constituents
            ),
            cql,
            range,
        )

    def register(
        self,
        reference_type: str,
        input: Epodoc,
        constituents: Optional[List[str]] = None,
    ) -> requests.Response:
        """
        Provides the interface for the European Patent Register online service for retrieving all
        the publicly available information on published European patent applications and
        international PCT applications designating the EPO as they pass through the grant procedure.

        Possible constituents: "biblio", "events", "procedural-steps" or "upp".

        Notes:
        1) Only the Epodoc input format is supported
        2) the default behaviour of the register retrieval is biblio, so you don't have to add the
           biblio constituent if you want to retrieve only bibliographic data.
        """
        # TODO: input can only be Epodoc, not Docdb
        constituents = constituents or ["biblio"]
        return self._service_request(
            dict(
                service=self.__register_path__,
                reference_type=reference_type,
                input=input,
                constituents=constituents,
            )
        )

    def register_search(
        self, cql: str, range_begin: int = 1, range_end: int = 25
    ) -> requests.Response:
        """
        Use this service to find specific register data
        that is part of the public aspect of the patent lifecycle.

        Example:
            >>> response = client.register_search(cql="pa=IBM", range_begin=1, range_end=25)
            >>> print(response.text)

        """
        range = dict(key="Range", begin=range_begin, end=range_end)
        return self._search_request(
            {"service": self.__register_search_path__}, cql, range
        )

    @property
    def access_token(self):
        # TODO: Custom auth handler plugin to requests?
        if (not self._access_token) or (
            self._access_token and self._access_token.is_expired
        ):
            self._acquire_token()
        return self._access_token

    def _acquire_token(self):
        headers = {
            "Authorization": "Basic {0}".format(
                b64encode(
                    "{0}:{1}".format(self.key, self.secret).encode("ascii")
                ).decode("ascii")
            ),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {"grant_type": "client_credentials"}
        response = requests.post(
            self.__auth_url__, headers=headers, data=payload, timeout=NETWORK_TIMEOUT
        )
        response.raise_for_status()
        self._access_token = AccessToken(response)

    def _check_for_exceeded_quota(self, response):
        if (response.status_code != requests.codes.forbidden) or (
            "X-Rejection-Reason" not in response.headers
        ):
            return response

        reasons = ("IndividualQuotaPerHour", "RegisteredQuotaPerWeek")

        rejection = response.headers["X-Rejection-Reason"]

        for reason in [r for r in reasons if r.lower() in rejection.lower()]:
            try:
                response.raise_for_status()
            except HTTPError as e:
                klass = getattr(exceptions, "{0}Exceeded".format(reason))
                e.__class__ = klass
                raise
        return response  # pragma: no cover

    def _make_request(self, url, data, extra_headers=None, params=None, use_get=False):
        token = "Bearer {0}".format(self.access_token.token)
        headers = {
            "Accept": self.accept_type,
            "Content-Type": "text/plain",
            "Authorization": token,
        }
        headers.update(extra_headers or {})
        request_method = self.request.post
        if use_get:
            request_method = self.request.get

        response = request_method(url, data=data, headers=headers, params=params)
        response = self._check_for_expired_token(response)
        response = self._check_for_exceeded_quota(response)
        response.raise_for_status()
        return response

    # info: {
    #   use_get?: boolean = False
    #   service?: string,
    #   reference_type?: string,
    #   input?: BaseInput | BaseInput[],
    #   endpoint?: string,
    #   constituents?: string[]
    # }
    def _make_request_url(self, info):
        _input = info.get("input", None)
        input_format = _input.__class__.__name__.lower() if _input else None
        constituents = info.get("constituents") or []

        parts_pre = [
            self.__service_url_prefix__,
            info.get("service", None),
            info.get("reference_type", None),
            input_format,
        ]
        parts_post = [info.get("endpoint", None), ",".join(constituents)]

        if info.get("use_get", False):
            parts = parts_pre + [_input.as_api_input()] + parts_post
        else:
            parts = parts_pre + parts_post

        return "/".join(filter(None, parts))

    # Service requests
    # info: {service, reference_type, input, endpoint, constituents}
    def _service_request(self, info):
        _input = info["input"]
        if isinstance(_input, list):
            data = "\n".join([i.as_api_input() for i in _input])
            info["input"] = _input[0]
        else:
            data = _input.as_api_input()

        url = self._make_request_url(info)
        return self._make_request(url, data)

    # info: {service, constituents}
    def _search_request(self, info, cql, range):
        url = self._make_request_url(info)
        return self._make_request(
            url, {"q": cql}, {range["key"]: "{begin}-{end}".format(**range)}
        )

    def _image_request(self, path, range, document_format):
        url = self._make_request_url({"service": self.__images_path__})
        params = {"Range": range}
        data = path.replace(self.__images_path__ + "/", "")
        return self._make_request(
            url, data=data, extra_headers={"Accept": document_format}, params=params
        )

    def _check_for_expired_token(self, response):
        if response.status_code != requests.codes.bad:
            return response

        # FIXME: S314 Using `xml` to parse untrusted data is known to be vulnerable to XML attacks; use `defusedxml` equivalents
        message = ET.fromstring(response.content)  # noqa: S314
        if message.findtext("message") == "invalid_access_token":
            self._acquire_token()
            response = self._make_request(response.request.url, response.request.body)
        return response
