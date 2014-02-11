from datetime import datetime
import json

from dateutil.tz import tzutc
import pytest

from epo_ops.utils.json import dumps, loads


@pytest.fixture
def datetimes():
    return [
        datetime(2014, 2, 5, 18, 15, 24, 474846, tzinfo=tzutc()),
        datetime(2014, 2, 5, 18, 16, 24, 474846, tzinfo=tzutc()),
    ]


@pytest.fixture
def throttle_status_base():
    return {
        'system_status': 'idle',  # idle, busy, overloaded
        'services': {
            'images': {}
        }
    }


@pytest.fixture
def service_status(datetimes):
    s = []
    for dt in datetimes:
        s.append({
            'timestamp': dt,
            'status': 'green',  # green, yellow, red, black
            'limit': 200,  # requests per minute
        })
    return s


@pytest.fixture
def service_status_json(datetimes):
    s = []
    for dt in datetimes:
        s.append({
            'timestamp': dt.isoformat(),
            'status': 'green',  # green, yellow, red, black
            'limit': 200,  # requests per minute
        })
    return s


@pytest.fixture
def throttle_status(datetimes, throttle_status_base, service_status):
    ts = throttle_status_base
    for dt in datetimes:
        ts['services']['images'] = service_status
    return ts


@pytest.fixture
def throttle_status_json(datetimes, throttle_status_base, service_status_json):
    ts = throttle_status_base
    for dt in datetimes:
        ts['services']['images'] = service_status_json
    return json.dumps(ts)


def test_encode_json_datetime(datetimes, throttle_status):
    status = dumps(throttle_status)
    for dt in datetimes:
        assert status.count(dt.isoformat())


def test_parse_json_datetime(datetimes, throttle_status_json):
    status = loads(throttle_status_json)
    for dt in datetimes:
        assert dt in [s['timestamp'] for s in status['services']['images']]


if __name__ == '__main__':
    pytest.main()
