# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import os
import urllib

from dateutil.tz import tzutc

from .exceptions import InvalidDate

log = logging.getLogger(__name__)


def makedirs(path, mode=0777):
    try:
        os.makedirs(path, mode)
    except OSError:
        pass


def now():
    return datetime.now(tzutc())


def quote(string):
    return urllib.quote(string, safe='/\\')


def validate_date(date):
    if date is None or date == '':
        return ''
    try:
        datetime.strptime(date, '%Y%m%d')
        return date
    except ValueError:
        raise InvalidDate('{} is not a valid YYYYMMDD date.'.format(date))
