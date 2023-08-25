import pytest
import responses
from pytest import raises

from epo_ops.exceptions import (
    IndividualQuotaPerHourExceeded,
    RegisteredQuotaPerWeekExceeded,
)
from epo_ops.models import Docdb


@pytest.fixture
def ops_backend_with_quota_exceeded():
    """
    Emulate an OPS backend, which returns responses on the corresponding
    endpoints that the per-hour and per-week service quotas have been exceeded.
    """
    token = responses.Response(
        responses.POST,
        url="https://ops.epo.org/3.2/auth/accesstoken",
        status=200,
        json={
            "access_token": "foo",
            "expires_in": 42,
        },
    )
    per_hour = responses.Response(
        responses.POST,
        url="https://ops.epo.org/3.2/rest-services/individual-per-hour-exceeded/publication/docdb/biblio",
        status=403,
        headers={
            "X-Rejection-Reason": "IndividualQuotaPerHour exceeded",
            "Content-Type": "application/xml",
        },
        body="<error><code>403</code><message>This request has been rejected due to the violation of Fair Use policy</message><moreInfo>http://www.epo.org/searching/free/espacenet/fair-use.html</moreInfo></error>",
    )
    per_week = responses.Response(
        responses.POST,
        url="https://ops.epo.org/3.2/rest-services/registered-per-week-exceeded/publication/docdb/biblio",
        status=403,
        headers={
            "X-Rejection-Reason": "RegisteredQuotaPerWeek exceeded",
            "Content-Type": "application/xml",
        },
        body="<error><code>403</code><message>This request has been rejected due to the violation of Fair Use policy</message><moreInfo>http://www.epo.org/searching/free/espacenet/fair-use.html</moreInfo></error>",
    )
    for response in [token, per_hour, per_week]:
        responses.add(response)


# Helpers
def issue_request(client):
    return client.published_data("publication", Docdb("1000000", "EP", "A1"))


# Tests
@responses.activate
def test_mock_quota_exceeded(ops_backend_with_quota_exceeded, all_clients, monkeypatch):
    errors = {
        "individual-per-hour-exceeded": IndividualQuotaPerHourExceeded,
        "registered-per-week-exceeded": RegisteredQuotaPerWeekExceeded,
    }

    for path, exception_class in errors.items():
        monkeypatch.setattr(all_clients, "__published_data_path__", path)
        with raises(exception_class):
            issue_request(all_clients)
