import logging

from .exceptions import MissingRequiredValue
from .utils import quote, validate_date

log = logging.getLogger(__name__)


def _prepare_part(part):
    return u'({})'.format(quote(part))


class BaseInput(object):
    def __init__(self, number, country_code, kind_code, date):
        if not all([number]):
            raise MissingRequiredValue(
                'number must be present'
            )
        self.number = number
        self.country_code = country_code
        self.kind_code = kind_code
        self.date = validate_date(date)

    def as_api_input(self):
        parts = filter(
            None, [self.country_code, self.number, self.kind_code, self.date]
        )
        return u'.'.join(map(_prepare_part, parts))


class Original(BaseInput):
    def __init__(self, number, country_code=None, kind_code=None, date=None):
        super(Original, self).__init__(number, country_code, kind_code, date)


class Docdb(BaseInput):
    def __init__(self, number, country_code, kind_code, date=None):
        if not all([country_code, kind_code]):
            raise MissingRequiredValue(
                'number, country_code, and kind_code must be present'
            )
        super(Docdb, self).__init__(number, country_code, kind_code, date)


class Epodoc(BaseInput):
    def __init__(self, number, kind_code=None, date=None):
        super(Epodoc, self).__init__(number, None, kind_code, date)
