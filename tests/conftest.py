import tempfile
import os

import pytest

from secrets import KEY, SECRET


def _storage(request):
    from epo_ops.throttle.storages import SQLite

    temp_db = tempfile.mkstemp()[1]

    def fin():
        os.remove(temp_db)
    request.addfinalizer(fin)

    return SQLite(temp_db)


@pytest.fixture()
def storage(request):
    return _storage(request)


@pytest.fixture(scope='module')
def module_storage(request):
    return _storage(request)


@pytest.fixture(scope='module')
def client(module_storage):
    from epo_ops import Client
    return Client(throttle_history_storage=module_storage)


@pytest.fixture(scope='module')
def registered_client(module_storage):
    from epo_ops import RegisteredClient
    return RegisteredClient(
        KEY, SECRET, throttle_history_storage=module_storage
    )
