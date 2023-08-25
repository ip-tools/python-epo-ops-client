from itertools import product

import pytest

from epo_ops.middlewares.throttle.storages import SQLite
from epo_ops.utils import now

from .helpers.sqlite_helpers import single_value_query, table_count


# Helpers
def single_col_query(storage, col):
    sql = "SELECT {0} FROM throttle_history LIMIT 1".format(col)
    return single_value_query(storage, sql)


# Tests
def test_columns_generation(cols):
    for service, field in product(SQLite.SERVICES, ("status", "limit", "retry_after")):
        assert "{0}_{1}".format(service, field) in cols


def test_columns_generation_with_types(storage):
    cols = storage.service_columns(True)
    for service, field in product(
        SQLite.SERVICES, ("status text", "limit integer", "retry_after integer")
    ):
        assert "{0}_{1}".format(service, field) in cols


def test_table_creation(storage, cols):
    for _i in range(10):  # Prepare as many times as we want!
        storage.prepare()
    with storage.db:
        c = storage.db.execute("SELECT * FROM throttle_history")
    db_cols = list(zip(*c.description))[0]
    expected = list(cols) + ["timestamp", "system_status"]
    assert sorted(db_cols) == sorted(expected)


def test_sqlite_timestamp_conversion(storage):
    dt = now()
    sql = "INSERT INTO throttle_history(timestamp) VALUES (?)"
    with storage.db:
        storage.db.execute(sql, (dt,))
    assert single_col_query(storage, "timestamp") == dt


def test_prune(storage, expired_timestamps, valid_timestamps):
    timestamps = expired_timestamps + valid_timestamps
    sql = "INSERT INTO throttle_history(timestamp) VALUES (?)"
    storage.db.executemany(sql, zip(timestamps))

    assert table_count(storage) == len(timestamps)
    storage.prune()
    assert table_count(storage) == len(valid_timestamps)


@pytest.mark.usefixtures("generate_sample_throttle_snapshot_reprs")
def test_parse_throttle_header(storage, throttle_snapshot):
    header = throttle_snapshot.as_header()
    expected = throttle_snapshot.as_dict()
    assert storage.parse_throttle(header) == expected


def test_update_with_header(storage, header, throttle_snapshot, retry_after_value):
    start = now()
    storage.update(header)
    assert table_count(storage) == 1
    assert now() > single_col_query(storage, "timestamp") > start
    assert single_col_query(storage, "system_status") == (
        throttle_snapshot.system_status
    )
    for s in throttle_snapshot.service_statuses:
        for service, (col, val) in product(
            [s.service], zip(("status", "limit"), (s.status, s.limit))
        ):
            col = "{0}_{1}".format(service, col)
            assert single_col_query(storage, col) == val

        if s.status.lower() == "black":
            col = "{0}_retry_after".format(s.service)
            assert single_col_query(storage, col) == retry_after_value


def test_delay_no_history(storage):
    assert table_count(storage) == 0
    for s in SQLite.SERVICES:
        assert storage.delay_for(s) == 0


def test_delay_expired_history(expired_throttle_history):
    storage = expired_throttle_history
    for s in SQLite.SERVICES:
        assert storage.delay_for(s) == 0
    assert table_count(storage) == 0


def test_delay(throttle_history):
    storage = throttle_history["storage"]
    expected = throttle_history["expected"]
    for k, v in expected.items():
        # We round to account for db operation time
        assert round(storage.delay_for(k), 0) == round(v, 0)
    assert table_count(storage) == 5
