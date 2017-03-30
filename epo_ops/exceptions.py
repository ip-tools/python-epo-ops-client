# -*- coding: utf-8 -*-

import logging

from requests.exceptions import HTTPError

log = logging.getLogger(__name__)


# Query errors
class InvalidDate(ValueError):
    """User used an invalid date."""


class MissingRequiredValue(ValueError):
    """User did not supply a required value."""


# Number service error
class InvalidNumberConversion(ValueError):
    """Invalid number conversion request."""


# OPS quota errors
class IndividualQuotaPerHourExceeded(HTTPError):
    """Quota per hour (approx 450MB) exceeded."""


class RegisteredQuotaPerWeekExceeded(HTTPError):
    """Quota per week (2.5GB) exceeded."""
