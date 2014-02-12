from time import sleep
import logging

import requests

from .utils import service_for_url

log = logging.getLogger(__name__)


class Throttler(object):
    def __init__(self, history_file):
        self.throttle_history = ThrottleHistory(history_file)

    def post(self, url, data=None, **kwargs):
        service = service_for_url(url)
        sleep(self.throttle_history.delay_for(service))
        response = requests.post(url, data, **kwargs)
        self.throttle_history.update(response.headers)
        return response


class ThrottleHistory(object):
    def __init__(self, history_file):
        self.history_file = history_file

    @property
    def base(self):
        return {
            'system_status': 'idle',  # idle, busy, overloaded
            'services': {},
        }

    def delay_for(self, service):
        # look up service from history and calculate delay
        return 1

    def update(self, headers):
        # prune and update the history file
        pass
