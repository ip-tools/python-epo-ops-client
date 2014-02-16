import tempfile
import os

import pytest

from epo_ops.throttle.storages import SQLite


def _storage(request):
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
