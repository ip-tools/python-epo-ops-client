from time import sleep
import logging

import requests

from .utils import service_for_url

log = logging.getLogger(__name__)


class Throttler(object):
    def __init__(self, history_storage):
        self.history = history_storage

    def post(self, url, data=None, **kwargs):
        service = service_for_url(url)
        sleep(self.history.delay_for(service))
        response = requests.post(url, data, **kwargs)
        self.history.update(response.headers)
        return response
