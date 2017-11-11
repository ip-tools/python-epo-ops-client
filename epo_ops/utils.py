# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime

from dateutil.tz import tzutc

from six.moves import urllib

from .exceptions import InvalidDate

log = logging.getLogger(__name__)


def makedirs(path, mode=0o777):
    try:
        os.makedirs(path, mode)
    except OSError:
        pass


def now():
    return datetime.now(tzutc())


def quote(string):
    return urllib.parse.quote(string, safe='/\\')


def validate_date(date):
    if date is None or date == '':
        return ''
    try:
        datetime.strptime(date, '%Y%m%d')
        return date
    except ValueError:
        raise InvalidDate('{0} is not a valid YYYYMMDD date.'.format(date))
