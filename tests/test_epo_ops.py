from datetime import datetime

from pytest import raises
from requests.exceptions import HTTPError
import pytest

from epo_ops import Client, RegisteredClient
from epo_ops.models import Docdb

from secrets import KEY, SECRET


# Helpers
def issue_request(client):
    return client.published_data('publication', Docdb('1000000', 'EP', 'A1'))


def service_success(client):
    r = issue_request(client)
    assert r.status_code == 200
    assert r.headers['X-API'] == 'ops-v3.1'


# Fixtures
@pytest.fixture(scope='module')
def registered_client():
    return RegisteredClient(
        KEY, SECRET
    )


@pytest.fixture(scope='module')
def mock_anonymous_client():
    c = Client()
    c.__service_url_prefix__ = 'https://opsv31.apiary.io'
    return c


# Tests
def test_real_happy_anonymous():
    service_success(Client())


def test_mock_happy_anonymous(mock_anonymous_client):
    mock_anonymous_client.__published_data__ = 'anonymous-success'
    service_success(mock_anonymous_client)


def test_real_get_access_token(registered_client):
    assert 'access_token' in registered_client.access_token._content


def test_real_happy_registered(registered_client):
    service_success(registered_client)


def test_real_400_invalid_token(registered_client):
    # Put in a token that's invalid, the server will raise 400
    registered_client.access_token.token = 'x34NdKmpABZ8ukqi4juRNQCrv5C5'
    with raises(HTTPError):
        issue_request(registered_client)


def test_real_400_expired_token(registered_client):
    # Put in a token that's expired, the server will raise 400 but we should
    # handle it gracefully
    registered_client.access_token.token = 'm34NdKmpABZ8ukqi4juRNQCrv5C5'
    service_success(registered_client)


def test_real_self_check_expired_token(registered_client):
    old_token = registered_client.access_token.token
    registered_client.access_token.expiration = datetime.now()
    assert old_token != registered_client.access_token.token


if __name__ == '__main__':
    pytest.main()
