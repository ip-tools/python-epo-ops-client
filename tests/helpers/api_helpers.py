from epo_ops.models import Docdb


def issue_published_data_request(client):
    return client.published_data('publication', Docdb('1000000', 'EP', 'A1'))


def assert_published_data_success(client):
    r = issue_published_data_request(client)
    assert r.status_code == 200
    assert r.headers['X-API'] == 'ops-v3.1'
