import pytest

from epo_ops.utils.json import dumps, loads


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
