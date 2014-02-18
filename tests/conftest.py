import tempfile
import os

import pytest

from secrets import KEY, SECRET


def _storage(request):
    from epo_ops.middlewares.throttle.storages import SQLite, sqlite

    temp_db = tempfile.mkstemp()[1]

    def fin():
        os.remove(temp_db)
    request.addfinalizer(fin)

    db = SQLite(temp_db)
    assert db.db_path != sqlite.DEFAULT_DB_PATH
    return db


@pytest.fixture()
def storage(request):
    return _storage(request)


@pytest.fixture(scope='module')
def module_storage(request):
    return _storage(request)


@pytest.fixture(scope='module')
def client(module_storage):
    from epo_ops import Client
    from epo_ops.middlewares import Throttler

    return Client(middlewares=[Throttler(module_storage)])


@pytest.fixture(scope='module')
def registered_client(module_storage):
    from epo_ops import RegisteredClient
    from epo_ops.middlewares import Throttler

    return RegisteredClient(
        KEY, SECRET, middlewares=[Throttler(module_storage)]
    )
