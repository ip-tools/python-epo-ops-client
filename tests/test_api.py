from datetime import datetime

from pytest import raises
from requests.exceptions import HTTPError
import pytest

from epo_ops.api import Client, RegisteredClient
from epo_ops.middlewares.throttle.storages import sqlite

from helpers.api_helpers import (
    assert_family_success, assert_published_data_search_success,
    assert_published_data_search_with_range_success,
    assert_published_data_success, issue_published_data_request
)


def test_instantiate_simple_client():
    client = Client()
    assert len(client.middlewares) == 1
    assert client.middlewares[0].history.db_path == sqlite.DEFAULT_DB_PATH

    client = RegisteredClient('key', 'secret')
    assert len(client.middlewares) == 1
    assert client.middlewares[0].history.db_path == sqlite.DEFAULT_DB_PATH


def test_published_data(all_clients):
    assert_published_data_success(all_clients)


def test_family(all_clients):
    assert_family_success(all_clients)


def test_published_data_search(all_clients):
    assert_published_data_search_success(all_clients)


def test_published_data_search_with_range(all_clients):
    assert_published_data_search_with_range_success(all_clients)


def test_get_access_token(registered_clients):
    assert 'access_token' in registered_clients.access_token._content


def test_400_invalid_token(default_registered_client):
    # Put in a token that's invalid, the server will raise 400
    token = 'x34NdKmpABZ8ukqi4juRNQCrv5C5'
    default_registered_client.access_token.token = token
    with raises(HTTPError):
        issue_published_data_request(default_registered_client)


def test_400_expired_token(default_registered_client):
    # Put in a token that's expired, the server will raise 400 but we should
    # handle it gracefully
    token = 'm34NdKmpABZ8ukqi4juRNQCrv5C5'
    default_registered_client.access_token.token = token
    assert_published_data_success(default_registered_client)


def test_self_check_expired_token(registered_clients):
    old_token = registered_clients.access_token.token
    registered_clients.access_token.expiration = datetime.now()
    assert old_token != registered_clients.access_token.token


if __name__ == '__main__':
    pytest.main()
