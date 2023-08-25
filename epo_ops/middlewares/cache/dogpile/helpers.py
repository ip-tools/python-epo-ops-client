# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def kwarg_range_header_handler(**kwargs):
    keys = []
    range_headers = {"X-OPS-Range", "Range"}
    headers = kwargs.get("headers", {})
    for header in range_headers & set(headers.keys()):
        keys.append("headers.{0}={1}".format(header, headers[header]))
    return "|".join(keys)
