# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def kwarg_data_handler(**kwargs):
    if 'data' not in kwargs:
        return ''
    return 'data={}'.format(kwargs['data'])


def kwarg_range_header_handler(**kwargs):
    headers = kwargs.get('headers', None)
    if (not headers) or 'X-OPS-Range' not in headers:
        return ''
    return 'headers.X-OPS-Range={}'.format(headers['X-OPS-Range'])
