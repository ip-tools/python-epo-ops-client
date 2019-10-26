# -*- coding: utf-8 -*-

import logging
import time

from ..middleware import Middleware
from .storages import SQLite
from .utils import service_for_url

log = logging.getLogger(__name__)


class Throttler(Middleware):
    def __init__(self, history_storage=None):
        self.history = history_storage or SQLite()

    def process_request(self, env, url, data, **kwargs):
        if not env["from-cache"]:
            service = service_for_url(url)
            time.sleep(self.history.delay_for(service))
        return url, data, kwargs

    def process_response(self, env, response):
        if not env["from-cache"]:
            self.history.update(response.headers)
        return response
