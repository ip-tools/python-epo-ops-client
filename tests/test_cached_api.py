import pytest

from .helpers.api_helpers import assert_published_data_success


def test_caching(cached_clients, monkeypatch):
    assert_published_data_success(cached_clients)
    monkeypatch.delattr('requests.post')
    for i in range(2):
        assert_published_data_success(cached_clients)


if __name__ == '__main__':
    pytest.main()
