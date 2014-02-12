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


# TODO: We can session scope these histories, that way we can randomly pick
# statuses based on the number of datetimes. How do we make sure there is at
# least one black?
@pytest.fixture
def images_history(datetimes, service_status):
    return ServiceHistory(
        'images', datetimes, (service_status.green, service_status.red)
    )


@pytest.fixture
def inpadoc_history(datetimes, service_status):
    return ServiceHistory(
        'inpadoc', datetimes, (service_status.red, service_status.yellow)
    )


@pytest.fixture
def other_history(datetimes, service_status):
    return ServiceHistory(
        'other', datetimes, (service_status.yellow, service_status.green)
    )


@pytest.fixture
def retrieval_history(datetimes, service_status):
    return ServiceHistory(
        'retrieval', datetimes, (service_status.red, service_status.green)
    )


@pytest.fixture
def search_history(datetimes, service_status):
    return ServiceHistory(
        'search', datetimes, (service_status.green, service_status.black)
    )


@pytest.fixture
def throttle_history(
    images_history, inpadoc_history, other_history, retrieval_history,
    search_history
):
    return ThrottleHistory(
        images_history, inpadoc_history, other_history, retrieval_history,
        search_history
    )


@pytest.fixture
def generate_sample_json(throttle_history):
    fpath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures',
        'throttle_history.json'
    )
    with open(fpath, 'w+', encoding='utf-8') as of:
        of.write(throttle_history.as_json())
