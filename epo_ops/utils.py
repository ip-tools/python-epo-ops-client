from datetime import datetime
import logging
import urllib

from .exceptions import InvalidDate

log = logging.getLogger(__name__)


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
