from datetime import datetime

from pytest import raises
from requests.exceptions import HTTPError
import pytest

from epo_ops.api import Client, RegisteredClient

from helpers.api_helpers import (
    assert_family_success, assert_published_data_search_success,
    assert_published_data_search_with_range_success,
    assert_published_data_success, issue_published_data_request
)


def _service_test(func, *clients):
    for c in clients:
        func(c)


def test_instantiate_simple_client():
    assert len(Client().middlewares) == 1
    assert len(RegisteredClient('key', 'secret').middlewares) == 1


def test_published_data(client, registered_client):
    _service_test(assert_published_data_success, client, registered_client)


def test_family(client, registered_client):
    _service_test(assert_family_success, client, registered_client)


def test_published_data_search(client, registered_client):
    _service_test(
        assert_published_data_search_success, client, registered_client
    )


def test_published_data_search_with_range(client, registered_client):
    _service_test(
        assert_published_data_search_with_range_success, client,
        registered_client
    )


def test_get_access_token(registered_client):
    assert 'access_token' in registered_client.access_token._content


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
