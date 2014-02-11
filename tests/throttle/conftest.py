from datetime import datetime
import json

from dateutil.tz import tzutc
import pytest


def status_generator(timestamp, status, limit, retry_after=None):
    return {
        'timestamp': timestamp,
        'status': status,
        'limit': limit,
        'retry_after': retry_after or 0,
    }


def status_dict(service, datetimes, service_status):
    statuses = []
    for dt, status in zip(datetimes, service_status):
        statuses.append(status_generator(dt, *status))
    return {
        service: statuses
    }


@pytest.fixture
def datetimes():
    return [
        datetime(2014, 2, 5, 18, 15, 24, 474846, tzinfo=tzutc()),
        datetime(2014, 2, 5, 18, 16, 24, 474846, tzinfo=tzutc()),
    ]


@pytest.fixture
def service_status():
    class Statuses(object):
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

    return Statuses()


@pytest.fixture
def throttle_status_base():
    return {
        'system_status': 'idle',  # idle, busy, overloaded
        'services': {
        }
    }


@pytest.fixture
def images_status(datetimes, service_status):
    return status_dict(
        'images', datetimes,
        (service_status.green, service_status.yellow)
    )


@pytest.fixture
def images_status_json(datetimes, service_status):
    return status_dict(
        'images', [dt.isoformat() for dt in datetimes],
        (service_status.green, service_status.yellow)
    )


@pytest.fixture
def throttle_status(throttle_status_base, images_status):
    ts = throttle_status_base
    ts['services'].update(images_status)
    return ts


@pytest.fixture
def throttle_status_json(throttle_status_base, images_status_json):
    ts = throttle_status_base
    ts['services'].update(images_status_json)
    return json.dumps(ts)
