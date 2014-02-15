from itertools import product
import os
import tempfile

import pytest

from epo_ops.throttle.storages import SQLite
from epo_ops.utils import now


def single_value_query(storage, *params):
    return storage.db.execute(*params).fetchone()[0]


def table_count(storage):
    sql = 'SELECT COUNT(*) FROM throttle_history'
    return single_value_query(storage, sql)


def single_col_query(storage, col):
    sql = 'SELECT {} FROM throttle_history LIMIT 1'.format(col)
    return single_value_query(storage, sql)


@pytest.fixture()
def storage(request):
    temp_db = tempfile.mkstemp()[1]

    def fin():
        os.remove(temp_db)
    request.addfinalizer(fin)

    return SQLite(temp_db)


@pytest.fixture()
def cols(storage):
    return storage.service_columns()


def test_columns_generation(cols):
    for service, field in product(
        SQLite.SERVICES, ('status', 'limit', 'retry_after')
    ):
        assert '{}_{}'.format(service, field) in cols


def test_columns_generation_with_types(storage):
    cols = storage.service_columns(True)
    for service, field in product(
        SQLite.SERVICES,
        ('status text', 'limit integer', 'retry_after integer')
    ):
        assert '{}_{}'.format(service, field) in cols


def test_table_creation(storage, cols):
    for i in range(10):  # Prepare as many times as we want!
        storage.prepare()
    with storage.db:
        c = storage.db.execute('SELECT * FROM throttle_history')
    db_cols = list(zip(*c.description)[0])
    expected = list(cols) + ['timestamp', 'system_status']
    assert sorted(db_cols) == sorted(expected)


def test_sqlite_timestamp_conversion(storage):
    dt = now()
    sql = 'INSERT INTO throttle_history(timestamp) VALUES (?)'
    with storage.db:
        storage.db.execute(sql, (dt,))
    assert single_col_query(storage, 'timestamp') == dt


def test_prune(storage, expired_timestamps, valid_timestamps):
    timestamps = expired_timestamps + valid_timestamps
    sql = 'INSERT INTO throttle_history(timestamp) VALUES (?)'
    storage.db.executemany(sql, zip(timestamps))

    assert table_count(storage) == len(timestamps)
    storage.prune()
    assert table_count(storage) == len(valid_timestamps)


@pytest.mark.usefixtures('generate_sample_throttle_history_reprs')
def test_parse_throttle_header(storage, throttle_history):
    header = throttle_history.as_header()
    expected = throttle_history.as_dict()
    assert storage.parse_throttle(header) == expected


def test_update_with_header(
    storage, header, throttle_history, retry_after_value
):
    start = now()
    storage.update(header)
    assert table_count(storage) == 1
    assert now() > single_col_query(storage, 'timestamp') > start
    assert single_col_query(storage, 'system_status') ==\
        throttle_history.system_status
    for s in throttle_history.service_statuses:
        for service, (col, val) in product(
            [s.service], zip(['status', 'limit'], s.service_status)
        ):
            col = '{}_{}'.format(service, col)
            assert single_col_query(storage, col) == val

        if s.service_status[0].lower() == 'black':
            col = '{}_retry_after'.format(s.service)
            assert single_col_query(storage, col) == retry_after_value
