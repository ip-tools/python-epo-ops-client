# -*- coding: utf-8 -*-

__title__ = 'python-epo-ops-client'
__version__ = '0.0.1'
__author__ = 'George Song'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 55 Minutes'


import logging

from .api import Client, RegisteredClient


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:  # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
