# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging

import requests

from .exceptions import MissingRequiredValue
from .utils import quote, validate_date

log = logging.getLogger(__name__)


def _prepare_part(part):
    return u'({0})'.format(quote(part))


class BaseInput(object):
    def __init__(self, number, country_code, kind_code, date):
        if not all([number]):
            raise MissingRequiredValue(
                'number must be present'
            )
        self.number = number
        self.country_code = country_code
        self.kind_code = kind_code
        self.date = validate_date(date)

    def as_api_input(self):
        parts = filter(
            None, [self.country_code, self.number, self.kind_code, self.date]
        )
        return u'.'.join(map(_prepare_part, parts))


class Original(BaseInput):
    def __init__(self, number, country_code=None, kind_code=None, date=None):
        super(Original, self).__init__(number, country_code, kind_code, date)


class Docdb(BaseInput):
    def __init__(self, number, country_code, kind_code, date=None):
        if not all([country_code, kind_code]):
            raise MissingRequiredValue(
                'number, country_code, and kind_code must be present'
            )
        super(Docdb, self).__init__(number, country_code, kind_code, date)


class Epodoc(BaseInput):
    def __init__(self, number, kind_code=None, date=None):
        super(Epodoc, self).__init__(number, None, kind_code, date)


class AccessToken(object):
    def __init__(self, response):
        self._content = response.json()
        self.response = response
        self.token = self._content['access_token']
        self.expiration = (
            datetime.now() +
            timedelta(seconds=int(self._content['expires_in']))
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
            'cache-key': None, 'from-cache': False, 'is-cached': False,
            'response': None
        }

    def reset_env(self):
        self.env = {}
        self.env.update(self.default_env)

    def post(self, url, data=None, **kwargs):
        self.reset_env()

        for mw in self.middlewares:
            url, data, kwargs = mw.process_request(
                self.env, url, data, **kwargs
            )

        response = self.env['response'] or requests.post(url, data, **kwargs)

        for mw in reversed(self.middlewares):
            response = mw.process_response(self.env, response)

        self.reset_env()
        return response
