from time import sleep
import logging

from dogpile.cache import make_region
import requests

from .utils import service_for_url

log = logging.getLogger(__name__)


def kwarg_data_handler(**kwargs):
    if 'data' not in kwargs:
        return ''
    return '{}={}'.format('data', kwargs['data'])


def kwarg_header_handler(**kwargs):
    headers = kwargs.get('headers', None)
    if (not headers) or 'X-OPS-Range' not in headers:
        return ''
    return '{}={}'.format('headers.X-OPS-Range', headers['X-OPS-Range'])


def kwargs_key_generator(kwargs_handlers, func):
    fname = func.__name__

    def generate_key(*args, **kwargs):
        key = [fname] + map(str, args)

        for handler in kwargs_handlers:
            s = handler(**kwargs)
            if s:
                key.append(s)

        return '|'.join(key)
    return generate_key


region = make_region(function_key_generator=kwargs_key_generator).configure(
    'dogpile.cache.dbm',
    expiration_time=3600,
    arguments={
        'filename': '/var/tmp/python-epo-ops-client/cache.dbm',
    }
)


class Throttler(object):
    def __init__(self, history_storage):
        self.history = history_storage

    def __str__(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)

    @region.cache_on_arguments(
        namespace=[kwarg_data_handler, kwarg_header_handler]
    )
    def post(self, url, data=None, **kwargs):
        service = service_for_url(url)
        sleep(self.history.delay_for(service))
        response = requests.post(url, data, **kwargs)
        self.history.update(response.headers)
        return response
