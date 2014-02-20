# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

from dogpile.cache import make_region
from dogpile.cache.api import NO_VALUE
import requests

from .... import __version__
from ...middleware import Middleware
from .helpers import kwarg_range_header_handler

log = logging.getLogger(__name__)

DEFAULT_DBM_PATH = '/var/tmp/python-epo-ops-client/cache.dbm'
DEFAULT_TIMEOUT = 604800  # 1 week in seconds


class Dogpile(Middleware):
    def __init__(self, region=None, kwargs_handlers=None):
        self.region = region
        if not self.region:
            self.region = make_region().configure(
                'dogpile.cache.dbm',
                expiration_time=DEFAULT_TIMEOUT,
                arguments={'filename': DEFAULT_DBM_PATH}
            )

        self.kwargs_handlers = kwargs_handlers
        if not self.kwargs_handlers:
            self.kwargs_handlers = [kwarg_range_header_handler]

    def generate_key(self, *args, **kwargs):
        key = ['epo-ops-{}'.format(__version__)] + map(str, args)

        for handler in self.kwargs_handlers:
            s = handler(**kwargs)
            if s:
                key.append(s)

        return '|'.join(key)

    def is_response_cacheable(self, response):
        return response.status_code == requests.codes.ok

    def process_request(self, env, url, data, **kwargs):
        key = self.generate_key(url, data, **kwargs)
        env['cache-key'] = key
        response = self.region.get(key)
        if response != NO_VALUE:
            env['from-cache'] = True
            env['response'] = response
        return url, data, kwargs

    def process_response(self, env, response):
        if (not env['from-cache']) and self.is_response_cacheable(response):
            self.region.set(env['cache-key'], response)
            env['is-cached'] = True
        return response
