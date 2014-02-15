from codecs import open
from datetime import timedelta
import os

import pytest
from requests.structures import CaseInsensitiveDict

from epo_ops.utils import makedirs, now

from .helpers.conftest_helpers import ServiceSnapshot, ThrottleSnapshot


def generate_timestamps(deltas):
    timestamps = []
    for d in deltas:
        timestamps.append(now() - timedelta(minutes=d))
    return timestamps


@pytest.fixture
def expired_timestamps():
    deltas = (2, 1.5)
    return generate_timestamps(deltas)


@pytest.fixture
def valid_timestamps():
    deltas = (.75, .5, 0)
    return generate_timestamps(deltas)


@pytest.fixture
def service_status():
    class ServiceStatus(object):
        @property
        def green(self):
            return ('green', 200)

        @property
        def yellow(self):
            return ('yellow', 50)

        @property
        def red(self):
            return ('red', 5)

        @property
        def black(self):
            return ('black', 0)

    return ServiceStatus()


@pytest.fixture
def retry_after_value():
    return 60000


@pytest.fixture
def throttle_history(service_status):
    return ThrottleSnapshot(
        'idle',
        ServiceSnapshot('images', service_status.green),
        ServiceSnapshot('inpadoc', service_status.yellow),
        ServiceSnapshot('other', service_status.red),
        ServiceSnapshot('retrieval', service_status.black),
        ServiceSnapshot('search', service_status.green),
    )


@pytest.fixture
def header(throttle_history, retry_after_value):
    return CaseInsensitiveDict((
        ('X-Throttling-Control', throttle_history.as_header()),
        ('Retry-After', retry_after_value)
    ))


@pytest.fixture
def generate_sample_throttle_history_reprs(throttle_history):
    "Generate sample header and dict representations"
    sample_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'sample'
    )
    makedirs(sample_path)
    fheader = os.path.join(sample_path, 'throttle_history.header')
    fdict = os.path.join(sample_path, 'throttle_history.dict')
    with open(fheader, 'w+', encoding='utf-8') as of:
        of.write(throttle_history.as_header())
    with open(fdict, 'w+', encoding='utf-8') as of:
        of.write(str(throttle_history.as_dict()))
