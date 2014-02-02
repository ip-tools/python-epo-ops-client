from datetime import datetime

import pytest

from epo_ops import Client, RegisteredClient
from epo_ops.models import Docdb

from secrets import KEY, SECRET


@pytest.fixture(scope='module')
def registered_client():
    return RegisteredClient(
        KEY, SECRET
    )


def test_real_happy_anonymous():
    c = Client()
    r = c.published_data('publication', Docdb('1000000', 'EP', 'A1'))
    assert r.status_code == 200
    assert r.headers['X-API'] == 'ops-v3.1'


def test_real_get_access_token(registered_client):
    assert 'access_token' in registered_client.access_token._content


def test_real_happy_registered(registered_client):
    r = registered_client.published_data(
        'publication', Docdb('1000000', 'EP', 'A1')
    )
    assert r.status_code == 200
    assert r.headers['X-API'] == 'ops-v3.1'


def test_self_check_expired_token(registered_client):
    old_token = registered_client.access_token.token
    registered_client.access_token.expiration = datetime.now()
    assert old_token != registered_client.access_token.token


if __name__ == '__main__':
    pytest.main()
