# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class Middleware(object):
    def process_request(self, env, url, data, **kwargs):
        # Do something. Return an actual response if you want the middleware
        # chain to stop processing requests
        # response = None
        # return url, args, kwargs, response
        raise NotImplementedError

    def process_response(self, env, response):
        # Do something.
        # return response
        raise NotImplementedError
