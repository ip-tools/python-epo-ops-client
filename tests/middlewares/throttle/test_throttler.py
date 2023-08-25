from epo_ops.middlewares.throttle import Throttler

from ...helpers.api_helpers import (
    assert_family_success,
    assert_published_data_success,
)
from .helpers.sqlite_helpers import table_count


def find_throttler(client):
    for mw in client.middlewares:
        if isinstance(mw, Throttler):
            return mw
    return None


def test_no_history_update_if_cached_response(reset_cached_clients):
    for _i in range(2):
        assert_family_success(reset_cached_clients)
    assert table_count(find_throttler(reset_cached_clients).history) == 1

    for _i in range(2):
        assert_published_data_success(reset_cached_clients)
    assert table_count(find_throttler(reset_cached_clients).history) == 2
