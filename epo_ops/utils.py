# -*- coding: utf-8 -*-

import logging
import os
import re
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
    parsed = urllib.parse.quote(string, safe="/\\")
    return re.sub(r"~", "%7E", parsed)


def validate_date(date):
    if date is None or date == "":
        return ""
    try:
        datetime.strptime(date, "%Y%m%d")
        return date
    except ValueError as exc:
        raise InvalidDate("{0} is not a valid YYYYMMDD date.".format(date)) from exc
