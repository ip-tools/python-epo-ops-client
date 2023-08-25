# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta

import requests

from .exceptions import MissingRequiredValue
from .utils import quote, validate_date

log = logging.getLogger(__name__)


NETWORK_TIMEOUT = 10.0


def _prepare_part(part):
    return "({0})".format(quote(part))


class BaseInput(object):
    def __init__(self, number, country_code, kind_code, date):
        if not number:
            raise MissingRequiredValue("number must be present")
        self.number = number
        self.country_code = country_code
        self.kind_code = kind_code
        self.date = validate_date(date)

    def as_api_input(self):
        parts = filter(
            None, [self.country_code, self.number, self.kind_code, self.date]
        )
        return ".".join(map(_prepare_part, parts))


class Original(BaseInput):
    def __init__(self, number, country_code=None, kind_code=None, date=None):
        super(Original, self).__init__(number, country_code, kind_code, date)


class Docdb(BaseInput):
    def __init__(self, number, country_code, kind_code, date=None):
        if not all([number, country_code, kind_code]):
            raise MissingRequiredValue(
                "number, country_code, and kind_code must be present"
            )
        super(Docdb, self).__init__(number, country_code, kind_code, date)


class Epodoc(BaseInput):
    def __init__(self, number, kind_code=None, date=None):
        super(Epodoc, self).__init__(number, None, kind_code, date)


class AccessToken(object):
    def __init__(self, response):
        self._content = response.json()
        self.response = response
        self.token = self._content["access_token"]
        self.expiration = datetime.now() + timedelta(
            seconds=int(self._content["expires_in"])
        )

    @property
    def is_expired(self):
        return datetime.now() >= self.expiration


class Request(object):
    def __init__(self, middlewares):
        self.middlewares = middlewares
        self.reset_env()

    @property
    def default_env(self):
        return {
            "cache-key": None,
            "from-cache": False,
            "is-cached": False,
            "response": None,
        }

    def reset_env(self):
        self.env = {}
        self.env.update(self.default_env)

    def post(self, url, data=None, **kwargs):
        return self._request(_post_callback, url, data, **kwargs)

    def get(self, url, data=None, **kwargs):
        return self._request(_get_callback, url, data, **kwargs)

    def _request(self, callback, url, data=None, **kwargs):
        self.reset_env()

        for mw in self.middlewares:
            url, data, kwargs = mw.process_request(self.env, url, data, **kwargs)

        # Either get response from cache environment or request from upstream
        # bool(<Response [200]>) is True
        # bool(<Response [404]>) is False
        response = self.env["response"] or callback(url, data, **kwargs)

        for mw in reversed(self.middlewares):
            response = mw.process_response(self.env, response)

        self.reset_env()
        return response


def _post_callback(url, data, **kwargs):
    return requests.post(url, data, **kwargs, timeout=NETWORK_TIMEOUT)


def _get_callback(url, data, **kwargs):
    return requests.get(url, **kwargs, timeout=NETWORK_TIMEOUT)
