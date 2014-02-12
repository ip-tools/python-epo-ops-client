from __future__ import absolute_import

import json
import logging

from dateutil.parser import parse

log = logging.getLogger(__name__)


def datetime_parser(dct):
    for k, v in dct.items():
        try:
            dt = parse(v)
            dct[k] = dt
        except:
            pass
    return dct


class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.isoformat()
        except:  # pragma: no cover
            return super(DateTimeJSONEncoder, self).default(obj)


def loads(s, **kwargs):
    kwargs.setdefault('object_hook', datetime_parser)
    return json.loads(s, **kwargs)


def dumps(obj, **kwargs):
    kwargs.setdefault('cls', DateTimeJSONEncoder)
    return json.dumps(obj, **kwargs)
