from datetime import datetime

from pytest import raises
from requests.exceptions import HTTPError
import pytest

from epo_ops import Client, RegisteredClient

from secrets import KEY, SECRET
from helpers.api_helpers import (
    assert_published_data_success, issue_published_data_request,
    assert_family_success, issue_family_request,
)


@pytest.fixture(scope='module')
def registered_client(module_storage):
    return RegisteredClient(
        KEY, SECRET, throttle_history_storage=module_storage
    )


def test_anonymous_published_data(storage):
    assert_published_data_success(Client(throttle_history_storage=storage))


def test_get_access_token(registered_client):
    assert 'access_token' in registered_client.access_token._content


def test_registered_published_data(registered_client):
    assert_published_data_success(registered_client)


def test_400_invalid_token(registered_client):
    # Put in a token that's invalid, the server will raise 400
    registered_client.access_token.token = 'x34NdKmpABZ8ukqi4juRNQCrv5C5'
    with raises(HTTPError):
        issue_published_data_request(registered_client)


def test_400_expired_token(registered_client):
    # Put in a token that's expired, the server will raise 400 but we should
    # handle it gracefully
    registered_client.access_token.token = 'm34NdKmpABZ8ukqi4juRNQCrv5C5'
    assert_published_data_success(registered_client)


def test_self_check_expired_token(registered_client):
    old_token = registered_client.access_token.token
    registered_client.access_token.expiration = datetime.now()
    assert old_token != registered_client.access_token.token


if __name__ == '__main__':
    pytest.main()
