from pytest import raises
import pytest

from epo_ops import Client
from epo_ops.exceptions import (
    AnonymousQuotaPerDayExceeded, AnonymousQuotaPerMinuteExceeded
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
def test_mock_anonymous_per_min_exceeded(mock_anonymous_client):
    mock_anonymous_client.__published_data_path__ = \
        'anonymous-per-min-exceeded'
    with raises(AnonymousQuotaPerMinuteExceeded):
        issue_request(mock_anonymous_client)


def test_mock_anonymous_per_day_exceeded(mock_anonymous_client):
    mock_anonymous_client.__published_data_path__ = \
        'anonymous-per-day-exceeded'
    with raises(AnonymousQuotaPerDayExceeded):
        issue_request(mock_anonymous_client)


if __name__ == '__main__':
    pytest.main()
