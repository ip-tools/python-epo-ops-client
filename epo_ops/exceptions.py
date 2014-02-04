from requests.exceptions import HTTPError


# Query errors
class InvalidDate(ValueError):
    """User used an invalid date."""


class MissingRequiredValue(ValueError):
    """User did not supply a required value."""


# OPS quota errors
class AnonymousQuotaPerMinuteExceeded(HTTPError):
    """Anonymous per minute quota exceeded."""


class AnonymousQuotaPerDayExceeded(HTTPError):
    """Anonymous per day quota exceeded."""
