from datetime import datetime
import logging
import os
import urllib

from .exceptions import InvalidDate

log = logging.getLogger(__name__)


def make_service_request_url(
    client, service, reference_type, input, endpoint, constituents
):
    parts = [
        client.__service_url_prefix__, service, reference_type,
        input.__class__.__name__.lower(), endpoint, ','.join(constituents)
    ]
    return os.path.join(*filter(None, parts))


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
