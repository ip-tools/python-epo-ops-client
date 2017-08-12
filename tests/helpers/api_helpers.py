import re

import requests

from epo_ops.models import Docdb
from epo_ops.models import Epodoc
from epo_ops.models import Original

data = ('publication', Docdb('1000000', 'EP', 'A1'))
rdata = ('publication', Epodoc('EP1000000'))
idata = ('published-data/images/EP/1000000/A1/fullimage', 1)
# idata path is the result @path from images published-data json request


def find_range(document, pattern):
    return re.search("range.*{0}".format(pattern), document)


def assert_request_success(response):
    assert response.status_code == requests.codes.ok
    assert response.headers['X-API'] == 'ops-v3.2'


def assert_family_success(client):
    response = client.family(*data)
    assert_request_success(response)
    assert 'patent-family' in response.text
    return response


def assert_image_success(client):
    response = client.image(*idata)
    assert_request_success(response)
    return response


def issue_published_data_request(client):
    return client.published_data(*data)


def assert_published_data_success(client):
    response = issue_published_data_request(client)
    assert_request_success(response)
    assert 'bibliographic-data' in response.text
    return response


def assert_published_data_search_success(client):
    response = client.published_data_search('applicant=IBM')
    assert_request_success(response)
    assert 'biblio-search' in response.text
    return response


def assert_published_data_search_with_range_success(client):
    response = client.published_data_search('applicant=IBM', 5, 6)
    assert find_range(response.text, 'begin="5"')
    assert find_range(response.text, 'end="6"')

    # Second time to make sure our cache key works properly
    response = client.published_data_search('applicant=IBM', 50, 60)
    assert_request_success(response)
    assert 'biblio-search' in response.text
    assert find_range(response.text, 'begin="50"')
    assert find_range(response.text, 'end="60"')
    return response


def assert_register_success(client):
    response = client.register(*rdata)
    assert_request_success(response)
    assert 'bibliographic-data' in response.text
    return response


def assert_register_search_success(client):
    response = client.register_search('applicant=IBM')
    assert_request_success(response)
    assert 'register-documents' in response.text
    return response


def assert_register_search_with_range_success(client):
    response = client.register_search('applicant=IBM', 5, 6)
    assert find_range(response.text, 'begin="5"')
    assert find_range(response.text, 'end="6"')

    response = client.register_search('applicant=IBM', 50, 60)
    assert_request_success(response)
    assert 'register-documents' in response.text
    assert find_range(response.text, 'begin="50"')
    assert find_range(response.text, 'end="60"')
    return response


def issue_number_request(client, output_format):
    return client.number(
        'application',
        Original('2006-147056', country_code='JP', kind_code='A'),
        output_format
    )


def assert_number_service_success(client):
    response = issue_number_request(client, 'docdb')
    assert 'ops:standardization' in response.text
    return response
