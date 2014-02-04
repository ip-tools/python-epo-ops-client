from base64 import b64encode
import logging
import xml.etree.ElementTree as ET

from requests.exceptions import HTTPError
import requests

from . import exceptions
from .models import AccessToken
from .utils import make_service_request_url

log = logging.getLogger(__name__)


class Client(object):
    __auth_url__ = 'https://ops.epo.org/3.1/auth/accesstoken'
    __service_url_prefix__ = 'https://ops.epo.org/3.1/rest-services'
    __published_data_path__ = 'published-data'

    def __init__(self, accept_type='xml'):
        self.accept_type = 'application/{}'.format(accept_type)

    def check_for_exceeded_quota(self, response):
        if (response.status_code != 403) or \
           ('X-Rejection-Reason' not in response.headers):
            return response

        reasons = (
            'AnonymousQuotaPerMinute',
            'AnonymousQuotaPerDay',
        )

        rejection = response.headers['X-Rejection-Reason']

        for reason in reasons:
            if reason.lower() in rejection.lower():
                try:
                    response.raise_for_status()
                except HTTPError as e:
                    klass = getattr(exceptions, '{}Exceeded'.format(reason))
                    e.__class__ = klass
                    raise
        return response

    def issue_request(self, url, data, extra_headers=None):
        headers = {'Accept': self.accept_type}
        headers.update(extra_headers or {})
        return requests.post(url, data=data, headers=headers)

    def make_request(self, url, data):
        response = self.issue_request(url, data)
        response = self.check_for_exceeded_quota(response)
        response.raise_for_status()
        return response

    def published_data(
        self, reference_type, input, endpoint='biblio', constituents=None
    ):
        if constituents is None:
            constituents = []

        url = make_service_request_url(
            self, self.__published_data_path__, reference_type, input,
            endpoint, constituents
        )
        return self.make_request(url, input.as_api_input())


class RegisteredClient(Client):
    def __init__(self, key, secret, accept_type='xml'):
        super(RegisteredClient, self).__init__(accept_type)
        self.key = key
        self.secret = secret
        self._access_token = None

    def acquire_token(self):
        headers = {
            'Authorization': 'Basic {}'.format(
                b64encode('{}:{}'.format(self.key, self.secret))
            ),
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {'grant_type': 'client_credentials'}
        response = requests.post(
            self.__auth_url__, headers=headers, data=payload
        )
        response.raise_for_status()
        self._access_token = AccessToken(response)

    @property
    def access_token(self):
        #TODO: Custom auth handler plugin to requests?
        if (not self._access_token) or \
           (self._access_token and self._access_token.is_expired):
            self.acquire_token()
        return self._access_token

    def check_for_expired_token(self, response):
        if response.status_code != 400:
            return response

        message = ET.fromstring(response.content)
        if message.findtext('description') == 'Access token has expired':
            self.acquire_token()
            response = self.make_request(
                response.request.url, response.request.body
            )
        return response

    def make_request(self, url, data):
        response = self.issue_request(
            url, data,
            {'Authorization': 'Bearer {}'.format(self.access_token.token)}
        )
        response = self.check_for_expired_token(response)
        response.raise_for_status()
        return response
