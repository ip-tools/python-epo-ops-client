# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class Storage(object):
    def delay_for(self, service):
        """
        This method accepts the name of a service, and return back number of
        seconds Throttler should wait before processing the request. Take care
        to observe the one minute sliding window.
        """
        raise NotImplementedError

    def update(self, headers):
        """
        This method accepts a requests.Response.headers object, or any other
        dictionary-like object that contains the the keys
        'x-throttling-control' and (optionally) 'retry-after'. It updates the
        throttle history storage backend appropriately.
        """
        raise NotImplementedError
