from pytest import raises
import pytest

from epo_ops import Client
from epo_ops.exceptions import (
    AnonymousQuotaPerDayExceeded, AnonymousQuotaPerMinuteExceeded,
    IndividualQuotaPerHourExceeded, RegisteredQuotaPerWeekExceeded
)
from epo_ops.models import Docdb


# Helpers
def issue_request(client):
    return client.published_data(
        'publication',
        Docdb('Quota', 'Forbidden', 'exceeded')
    )


@pytest.fixture(scope='module')
def mock_anonymous_client():
    c = Client()
    c.__service_url_prefix__ = 'https://opsv31.apiary.io'
    return c


# Tests
def test_mock_quota_exceeded(mock_anonymous_client):
    errors = {
        'anonymous-per-min-exceeded': AnonymousQuotaPerMinuteExceeded,
        'anonymous-per-day-exceeded': AnonymousQuotaPerDayExceeded,
        'individual-per-hour-exceeded': IndividualQuotaPerHourExceeded,
        'registered-per-week-exceeded': RegisteredQuotaPerWeekExceeded,
    }

    for path, exception_class in errors.items():
        mock_anonymous_client.__published_data_path__ = path
        with raises(exception_class):
            issue_request(mock_anonymous_client)


if __name__ == '__main__':
    pytest.main()
