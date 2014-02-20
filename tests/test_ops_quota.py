from pytest import raises
import pytest

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


# Tests
def test_mock_quota_exceeded(all_clients, monkeypatch):
    monkeypatch.setattr(
        all_clients, '__service_url_prefix__', 'https://opsv31.apiary.io'
    )
    errors = {
        'anonymous-per-min-exceeded': AnonymousQuotaPerMinuteExceeded,
        'anonymous-per-day-exceeded': AnonymousQuotaPerDayExceeded,
        'individual-per-hour-exceeded': IndividualQuotaPerHourExceeded,
        'registered-per-week-exceeded': RegisteredQuotaPerWeekExceeded,
    }

    for path, exception_class in errors.items():
        monkeypatch.setattr(
            all_clients, '__published_data_path__', path
        )
        with raises(exception_class):
            issue_request(all_clients)


if __name__ == '__main__':
    pytest.main()
