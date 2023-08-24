import pytest
from pytest import raises

from epo_ops.exceptions import (
    IndividualQuotaPerHourExceeded,
    RegisteredQuotaPerWeekExceeded,
)
from epo_ops.models import Docdb

from .secrets import APIARY_URL


# Helpers
def issue_request(client):
    return client.published_data("publication", Docdb("Quota", "Forbidden", "exceeded"))


# Tests
def test_mock_quota_exceeded(all_clients, monkeypatch):
    monkeypatch.setattr(all_clients, "__service_url_prefix__", APIARY_URL)
    errors = {
        "individual-per-hour-exceeded": IndividualQuotaPerHourExceeded,
        "registered-per-week-exceeded": RegisteredQuotaPerWeekExceeded,
    }

    for path, exception_class in errors.items():
        monkeypatch.setattr(all_clients, "__published_data_path__", path)
        with raises(exception_class):
            issue_request(all_clients)


if __name__ == "__main__":
    pytest.main()
