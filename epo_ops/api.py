# -*- coding: utf-8 -*-
import logging
from base64 import b64encode
from xml.etree import ElementTree as ET

import requests
from requests.exceptions import HTTPError

from . import exceptions
from .middlewares import Throttler
from .models import NETWORK_TIMEOUT, AccessToken, Request

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

    def family(self, reference_type, input, endpoint=None, constituents=None):
        url = self._make_request_url(
            dict(
                service=self.__family_path__,
                reference_type=reference_type,
                input=input,
                endpoint=endpoint,
                constituents=constituents,
                use_get=True,
            )
        )
        return self._make_request(url, None, params=input.as_api_input(), use_get=True)

    def image(self, path, range=1, document_format="application/tiff"):
        return self._image_request(path, range, document_format)

    def number(self, reference_type, input, output_format):
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
        self, reference_type, input, endpoint="biblio", constituents=None
    ):
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
        self, cql, range_begin=1, range_end=25, constituents=None
    ):
        range = dict(key="X-OPS-Range", begin=range_begin, end=range_end)
        return self._search_request(
            dict(
                service=self.__published_data_search_path__, constituents=constituents
            ),
            cql,
            range,
        )

    def register(self, reference_type, input, constituents=None):
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

    def register_search(self, cql, range_begin=1, range_end=25):
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
