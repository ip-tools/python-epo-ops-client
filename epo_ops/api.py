import logging

import requests

from .utils import make_service_request_url

log = logging.getLogger(__name__)


class Client(object):
    __auth_url = 'https://ops.epo.org/3.1/auth/accesstoken'
    __service_url_prefix__ = 'https://ops.epo.org/3.1/rest-services'

    def __init__(self, accept_type='xml'):
        self.accept_type = 'application/{}'.format(accept_type)

    def make_request(self, url, data):
        headers = {'Accept': 'application/xml'}
        return requests.post(url, data=data, headers=headers)

    def published_data(
        self, reference_type, input, endpoint='biblio', constituents=None
    ):
        if constituents is None:
            constituents = []

        url = make_service_request_url(
            self, 'published-data', reference_type, input, endpoint,
            constituents
        )

        return self.make_request(url, input.as_api_input())


class RegisteredClient(Client):
    def __init__(self, key, secret, accept_type='xml'):
        super(RegisteredClient, self).__init__(accept_type)
        self.key = key
        self.secret = key
