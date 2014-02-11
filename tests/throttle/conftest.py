from codecs import open
from datetime import datetime
import os

from dateutil.tz import tzutc
import pytest

from .helpers.conftest_helpers import ServiceHistory, ThrottleHistory


@pytest.fixture
def datetimes():
    return [
        datetime(2014, 2, 5, 18, 15, 24, 474846, tzinfo=tzutc()),
        datetime(2014, 2, 5, 18, 16, 24, 474846, tzinfo=tzutc()),
    ]


@pytest.fixture
def service_status():
    class ServiceStatus(object):
        @property
        def green(self):
            return ('green', 200, None)

        @property
        def yellow(self):
            return ('yellow', 50, None)

        @property
        def red(self):
            return ('red', 5, None)

        @property
        def black(self):
            return ('black', 0, 60)

    return ServiceStatus()


@pytest.fixture
def images_history(datetimes, service_status):
    return ServiceHistory(
        'images', datetimes, (service_status.green, service_status.red)
    )


@pytest.fixture
def throttle_history(images_history):
    return ThrottleHistory(images_history)


@pytest.fixture
def generate_sample_json(throttle_history):
    fpath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures',
        'throttle_history.json'
    )
    with open(fpath, 'w+', encoding='utf-8') as of:
        of.write(throttle_history.as_json())
