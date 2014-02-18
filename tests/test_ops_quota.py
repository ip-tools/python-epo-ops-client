from itertools import product

from pytest import raises
import pytest

from epo_ops import Client, RegisteredClient
from epo_ops.exceptions import (
    AnonymousQuotaPerDayExceeded, AnonymousQuotaPerMinuteExceeded,
    IndividualQuotaPerHourExceeded, RegisteredQuotaPerWeekExceeded
)
from epo_ops.middlewares import Throttler
from epo_ops.models import Docdb

from secrets import KEY, SECRET


# Helpers
def issue_request(client):
    return client.published_data(
        'publication',
        Docdb('Quota', 'Forbidden', 'exceeded')
    )


def _mock(client):
    client.__service_url_prefix__ = 'https://opsv31.apiary.io'
    return client


@pytest.fixture(scope='module')
def mock_client(module_storage):
    client = Client(middlewares=[Throttler(module_storage)])
    return _mock(client)


@pytest.fixture(scope='module')
def mock_registered_client(module_storage):
    client = RegisteredClient(
        KEY, SECRET, middlewares=[Throttler(module_storage)]
    )
    return _mock(client)


# Tests
def test_mock_quota_exceeded(mock_client, mock_registered_client):
    errors = {
        'anonymous-per-min-exceeded': AnonymousQuotaPerMinuteExceeded,
        'anonymous-per-day-exceeded': AnonymousQuotaPerDayExceeded,
        'individual-per-hour-exceeded': IndividualQuotaPerHourExceeded,
        'registered-per-week-exceeded': RegisteredQuotaPerWeekExceeded,
    }

    a_list = product((mock_client, mock_registered_client), errors.items())
    for client, (path, exception_class) in a_list:
        client.__published_data_path__ = path
        with raises(exception_class):
            issue_request(client)


if __name__ == '__main__':
    pytest.main()
