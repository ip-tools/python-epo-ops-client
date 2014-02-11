import pytest

from epo_ops.utils.json import dumps, loads


@pytest.mark.usefixtures('generate_sample_json')
def test_encode_json_datetime(datetimes, throttle_history):
    status = dumps(throttle_history.as_dict())
    for dt in datetimes:
        assert status.count(dt.isoformat())


def test_parse_json_datetime(datetimes, throttle_history):
    status = loads(throttle_history.as_json())
    for dt in datetimes:
        assert dt in [s['timestamp'] for s in status['services']['images']]


if __name__ == '__main__':
    pytest.main()
