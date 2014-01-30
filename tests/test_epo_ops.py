import pytest

from epo_ops import Client
from epo_ops.models import Docdb


def test_happy_anonymous():
    c = Client()
    r = c.published_data('publication', Docdb('1000000', 'EP', 'A1'))
    assert r.status_code == 200
    assert r.headers['X-API'] == 'ops-v3.1'


if __name__ == '__main__':
    pytest.main()
