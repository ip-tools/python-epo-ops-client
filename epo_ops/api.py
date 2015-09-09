# -*- coding: utf-8 -*-

from base64 import b64encode
import logging
import xml.etree.ElementTree as ET

from requests.exceptions import HTTPError
import requests

from . import exceptions
from .middlewares import Throttler
from .models import AccessToken, Request

log = logging.getLogger(__name__)


class Client(object):
    __auth_url__ = 'https://ops.epo.org/3.1/auth/accesstoken'
    __service_url_prefix__ = 'https://ops.epo.org/3.1/rest-services'

    __family_path__ = 'family'
    __published_data_path__ = 'published-data'
    __published_data_search_path__ = 'published-data/search'
    __register_path__ = 'register'
    __register_search_path__ = 'register/search'

    def __init__(self, accept_type='xml', middlewares=None):
        self.accept_type = 'application/{0}'.format(accept_type)
        self.middlewares = middlewares
        if middlewares is None:
            self.middlewares = [Throttler()]
        self.request = Request(self.middlewares)

    def _check_for_exceeded_quota(self, response):
        if (response.status_code != requests.codes.forbidden) or \
           ('X-Rejection-Reason' not in response.headers):
            return response

        reasons = (
            'AnonymousQuotaPerMinute',
            'AnonymousQuotaPerDay',
            'IndividualQuotaPerHour',
            'RegisteredQuotaPerWeek',
        )

        rejection = response.headers['X-Rejection-Reason']

        for reason in [r for r in reasons if r.lower() in rejection.lower()]:
            try:
                response.raise_for_status()
            except HTTPError as e:
                klass = getattr(exceptions, '{0}Exceeded'.format(reason))
                e.__class__ = klass
                raise
        return response  # pragma: no cover

    def _post(self, url, data, extra_headers=None):
        headers = {'Accept': self.accept_type}
        headers.update(extra_headers or {})
        return self.request.post(url, data=data, headers=headers)

    def _make_request(self, url, data, extra_headers=None):
        response = self._post(url, data, extra_headers)
        response = self._check_for_exceeded_quota(response)
        response.raise_for_status()
        return response

    def _make_request_url(
        self, service, reference_type, input, endpoint, constituents
    ):
        constituents = constituents or []
        parts = [
            self.__service_url_prefix__, service, reference_type,
            input and input.__class__.__name__.lower(), endpoint,
            ','.join(constituents)
        ]
        return u'/'.join(filter(None, parts))

    # Service requests
    def _service_request(
        self, path, reference_type, input, endpoint, constituents
    ):
        url = self._make_request_url(
            path, reference_type, input, endpoint, constituents
        )
        return self._make_request(url, input.as_api_input())

    def _search_request(self, path, cql, range, constituents=None):
        url = self._make_request_url(path, None, None, None, constituents)
        return self._make_request(
            url,
            {'q': cql},
            {range['key']: '{begin}-{end}'.format(**range)}
        )

    def family(self, reference_type, input, endpoint=None, constituents=None):
        return self._service_request(
            self.__family_path__, reference_type, input, endpoint, constituents
        )

    def published_data(
        self, reference_type, input, endpoint='biblio', constituents=None
    ):
        return self._service_request(
            self.__published_data_path__, reference_type, input, endpoint,
            constituents
        )

    def published_data_search(
        self, cql, range_begin=1, range_end=25, constituents=None
    ):
        range = dict(key='X-OPS-Range', begin=range_begin, end=range_end)
        return self._search_request(
            self.__published_data_search_path__, cql, range, constituents
        )

    def register(self, reference_type, input, constituents=None):
        # TODO: input can only be Epodoc, not Docdb
        constituents = constituents or ['biblio']
        return self._service_request(
            self.__register_path__, reference_type, input, None, constituents
        )

    def register_search(self, cql, range_begin=1, range_end=25):
        range = dict(key='Range', begin=range_begin, end=range_end)
        return self._search_request(self.__register_search_path__, cql, range)


class RegisteredClient(Client):
    def __init__(
        self, key, secret, accept_type='xml', middlewares=None
    ):
        super(RegisteredClient, self).__init__(accept_type, middlewares)
        self.key = key
        self.secret = secret
        self._access_token = None

    def _acquire_token(self):
        headers = {
            'Authorization': 'Basic {0}'.format(
                b64encode(
                    '{0}:{1}'.format(self.key, self.secret).encode('ascii')
                ).decode('ascii')
            ),
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {'grant_type': 'client_credentials'}
        response = requests.post(
            self.__auth_url__, headers=headers, data=payload
        )
        response.raise_for_status()
        self._access_token = AccessToken(response)

    def _check_for_expired_token(self, response):
        if response.status_code != requests.codes.bad:
            return response

        message = ET.fromstring(response.content)
        if message.findtext('description') == 'Access token has expired':
            self._acquire_token()
            response = self._make_request(
                response.request.url, response.request.body
            )
        return response

    def _make_request(self, url, data, extra_headers=None):
        extra_headers = extra_headers or {}
        token = 'Bearer {0}'.format(self.access_token.token)
        extra_headers['Authorization'] = token

        response = self._post(url, data, extra_headers)
        response = self._check_for_expired_token(response)
        response = self._check_for_exceeded_quota(response)
        response.raise_for_status()
        return response

    @property
    def access_token(self):
        # TODO: Custom auth handler plugin to requests?
        if (not self._access_token) or \
           (self._access_token and self._access_token.is_expired):
            self._acquire_token()
        return self._access_token
