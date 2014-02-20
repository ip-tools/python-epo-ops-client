# -*- coding: utf-8 -*-

from time import sleep
import logging

from ..middleware import Middleware
from .utils import service_for_url

log = logging.getLogger(__name__)


class Throttler(Middleware):
    def __init__(self, history_storage):
        self.history = history_storage

    def __str__(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)

    def process_request(self, env, url, data, **kwargs):
        if not env['from-cache']:
            service = service_for_url(url)
            sleep(self.history.delay_for(service))
        return url, data, kwargs

    def process_response(self, env, response):
        if not env['from-cache']:
            self.history.update(response.headers)
        return response
