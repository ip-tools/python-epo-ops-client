from epo_ops.models import Docdb

data = ('publication', Docdb('1000000', 'EP', 'A1'))


def assert_request_success(response):
    assert response.status_code == 200
    assert response.headers['X-API'] == 'ops-v3.1'


def issue_published_data_request(client):
    return client.published_data(*data)


def assert_published_data_success(client):
    response = issue_published_data_request(client)
    assert_request_success(response)
    assert 'bibliographic-data' in response.text
    return response


def issue_family_request(client):
    return client.family(*data)


def assert_family_success(client):
    response = issue_family_request(client)
    assert_request_success(response)
    assert 'patent-family' in response.text
    return response


def issue_published_data_search_request(client):
    return client.published_data_search('applicant=IBM')


def assert_published_data_search_success(client):
    response = issue_published_data_search_request(client)
    assert_request_success(response)
    assert 'biblio-search' in response.text
    return response


def issue_published_data_search_request_with_range(client):
    return client.published_data_search('applicant=IBM', 50, 60)


def assert_published_data_search_with_range_success(client):
    response = issue_published_data_search_request_with_range(client)
    assert_request_success(response)
    assert 'biblio-search' in response.text
    assert 'range begin="50" end="60"' in response.text
    return response
