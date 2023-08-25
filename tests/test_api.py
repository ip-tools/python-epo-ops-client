from datetime import datetime

from pytest import raises

from epo_ops.api import Client
from epo_ops.exceptions import InvalidNumberConversion
from epo_ops.middlewares.throttle.storages import sqlite

from .helpers.api_helpers import (
    assert_bulk_service_retrival_success,
    assert_family_biblio_success,
    assert_family_legal_success,
    assert_family_success,
    assert_image_success,
    assert_number_service_success,
    assert_published_data_search_success,
    assert_published_data_search_with_range_success,
    assert_published_data_success,
    assert_register_search_success,
    assert_register_search_with_range_success,
    assert_register_success,
    issue_number_request,
)


def test_instantiate_simple_client():
    client = Client("key", "secret")
    assert len(client.middlewares) == 1
    assert client.middlewares[0].history.db_path == sqlite.DEFAULT_DB_PATH


def test_family(all_clients):
    assert_family_success(all_clients)


def test_family_biblio(all_clients):
    assert_family_biblio_success(all_clients)


def test_family_legal(all_clients):
    assert_family_legal_success(all_clients)


def test_image(all_clients):
    assert_image_success(all_clients)


def test_published_data(all_clients):
    assert_published_data_success(all_clients)


def test_published_data_search(all_clients):
    assert_published_data_search_success(all_clients)


def test_published_data_search_with_range(all_clients):
    assert_published_data_search_with_range_success(all_clients)


def test_bulk_published_data_retreval(all_clients):
    assert_bulk_service_retrival_success(all_clients)


def test_register(all_clients):
    assert_register_success(all_clients)


def test_register_search(all_clients):
    assert_register_search_success(all_clients)


def test_register_search_with_range(all_clients):
    assert_register_search_with_range_success(all_clients)


def test_number_service(all_clients):
    assert_number_service_success(all_clients)


def test_invalid_number_conversions(default_client):
    with raises(InvalidNumberConversion):
        issue_number_request(default_client, "original")


def test_get_access_token(clients):
    assert "access_token" in clients.access_token._content


def test_400_expired_or_inavlid_token(default_client):
    # Put in a token that's expired or invalid, the server will raise 400 but we
    # should handle it gracefully
    token = "m34NdKmpABZ8ukqi4juRNQCrv5C5"  # noqa: S105
    default_client.access_token.token = token
    assert_published_data_success(default_client)


def test_self_check_expired_token(clients):
    old_token = clients.access_token.token
    clients.access_token.expiration = datetime.now()
    assert old_token != clients.access_token.token


def test_caching(cached_clients, monkeypatch):
    assert_published_data_success(cached_clients)
    monkeypatch.delattr("requests.request")
    for _i in range(2):
        assert_published_data_success(cached_clients)


def test_throttling(non_cached_clients, monkeypatch):
    def mock_sleep(service):
        raise RuntimeError("Sleeping!")

    assert_published_data_success(non_cached_clients)
    monkeypatch.setattr("time.sleep", mock_sleep)
    with raises(RuntimeError):
        assert_published_data_success(non_cached_clients)
