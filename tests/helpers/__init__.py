import os
import shutil
import tempfile
from random import choice
from string import ascii_letters

from dogpile.cache import make_region


def mkfile(request):
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(
        temp_dir, "".join(choice(ascii_letters) for i in range(10))
    )

    def fin():
        shutil.rmtree(temp_dir)

    request.addfinalizer(fin)

    return temp_file


def mksqlite(request):
    from epo_ops.middlewares.throttle.storages import SQLite, sqlite

    db = SQLite(mkfile(request))
    assert db.db_path != sqlite.DEFAULT_DB_PATH
    return db


def mkthrottler(request):
    from epo_ops.middlewares import Throttler

    return Throttler(mksqlite(request))


def mkcache(request):
    from epo_ops.middlewares import Dogpile
    from epo_ops.middlewares.cache.dogpile import dogpile

    region = make_region().configure(
        "dogpile.cache.dbm",
        expiration_time=dogpile.DEFAULT_TIMEOUT,
        arguments={"filename": mkfile(request)},
    )

    return Dogpile(region)
