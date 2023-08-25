# -*- coding: utf-8 -*-

import os
from codecs import open
from datetime import timedelta
from pprint import pformat
from random import choice, shuffle

import pytest
from requests.structures import CaseInsensitiveDict

from epo_ops.middlewares.throttle.storages import SQLite
from epo_ops.utils import makedirs, now

from .helpers.conftest_helpers import ServiceSnapshot, ThrottleSnapshot


def generate_timestamps(deltas):
    return [now() - timedelta(minutes=d) for d in deltas]


def make_throttle_snapshot(system_status, services):
    snapshots = [
        ServiceSnapshot(service, status, limit)
        for service, (status, limit) in services.items()
    ]
    return ThrottleSnapshot(system_status, snapshots)


def make_header(control, retry=None):
    h = CaseInsensitiveDict({"X-Throttling-Control": control})
    if retry:
        h["Retry-After"] = retry
    return h


@pytest.fixture
def cols(storage):
    return storage.service_columns()


@pytest.fixture
def expired_timestamps():
    deltas = (2, 1.5)
    return generate_timestamps(deltas)


@pytest.fixture
def valid_timestamps():
    deltas = (0.75, 0.5, 0)
    return generate_timestamps(deltas)


@pytest.fixture
def service_status():
    class ServiceStatus(object):
        @property
        def green(self):
            return ("green", 200)

        @property
        def yellow(self):
            return ("yellow", 50)

        @property
        def red(self):
            return ("red", 5)

        @property
        def black(self):
            return ("black", 0)

    return ServiceStatus()


@pytest.fixture
def retry_after_value():
    return 60000


@pytest.fixture
def throttle_snapshot(service_status):
    return make_throttle_snapshot(
        "idle",
        {
            "images": service_status.green,
            "inpadoc": service_status.yellow,
            "other": service_status.red,
            "retrieval": service_status.black,
            "search": service_status.green,
        },
    )


@pytest.fixture
def header(throttle_snapshot, retry_after_value):
    return make_header(throttle_snapshot.as_header(), retry_after_value)


@pytest.fixture
def expired_throttle_history(storage, expired_timestamps):
    def _services_dict(limit):
        sd = {}
        for s in SQLite.SERVICES:
            sd[s] = ("green", limit)
        return sd

    limits = (1000, 2000)
    for limit in limits:
        snapshot = make_throttle_snapshot("idle", _services_dict(limit))
        storage.update(make_header(snapshot.as_header()))

    sql = "UPDATE throttle_history SET timestamp=? WHERE images_limit=?"
    for param in zip(expired_timestamps, limits):
        storage.db.execute(sql, param)

    return storage


@pytest.fixture
def throttle_history(expired_throttle_history, retry_after_value):
    """
    Contains multiple randomly generated throttle snapshots in storage. There
    is one snapshot where search service has black status and a retry-after
    value.
    """
    storage = expired_throttle_history
    system_stats = ("idle", "busy", "overloaded")
    lights = ("green", "yellow", "red")
    sample_count = 4
    expected = {}
    service_limits = {}

    def _range(end, step=-10):
        start = end + -step * (sample_count - 1)
        return range(start, end - 1, step)

    def _services_dicts(limits):
        snapshots = []
        for i in range(sample_count):
            sd = {}
            for k, v in limits.items():
                sd[k] = (choice(lights), v[i])
            snapshots.append(sd)
        return snapshots

    for service, limit in zip(SQLite.SERVICES, (200, 100, 60, 10, 5)):
        expected[service] = 60.0 / limit
        service_limits[service] = list(_range(limit))
        shuffle(service_limits[service])

    for d in _services_dicts(service_limits):
        storage.update(
            make_header(make_throttle_snapshot(choice(system_stats), d).as_header())
        )

    # Make a special header with search=black with retry value
    services = list(SQLite.SERVICES)
    services.remove("search")
    services = ", ".join(["{0}=green:1000".format(s) for s in services])
    storage.update(
        make_header(
            "{0} (search=black:0, {1})".format(choice(system_stats), services),
            retry_after_value,
        )
    )

    # Make sure to override expected
    expected["search"] = retry_after_value / 1000.0

    return {"expected": expected, "storage": storage}


@pytest.fixture
def generate_sample_throttle_snapshot_reprs(throttle_snapshot):
    "Generate sample header and dict representations"
    sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample")
    makedirs(sample_path)
    fheader = os.path.join(sample_path, "throttle_snapshot.header")
    fdict = os.path.join(sample_path, "throttle_snapshot.dict")
    with open(fheader, "wb+", encoding="utf-8") as of:
        of.write(throttle_snapshot.as_header())
    with open(fdict, "wb+", encoding="utf-8") as of:
        of.write(pformat(throttle_snapshot.as_dict()))
