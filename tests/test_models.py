from pytest import raises
import pytest

from epo_ops.exceptions import InvalidDate, MissingRequiredValue
from epo_ops.models import Docdb, Epodoc, Original


def test_original_required():
    with raises(MissingRequiredValue):
        Original('')


def test_docdb_required():
    with raises(MissingRequiredValue):
        Docdb('123', None, None)
    with raises(MissingRequiredValue):
        Docdb('123', '345', '')
    with raises(MissingRequiredValue):
        Docdb('', None, None)


def test_epodoc_required():
    with raises(MissingRequiredValue):
        Epodoc('')


def test_invalid_date():
    with raises(InvalidDate):
        Original('123', date='20141505')


def test_full_original_as_api_input():
    params = ['US08/921,321', 'CC', 'B2', '20140122']
    expected = '(CC).(US08/921%2C321).(B2).(20140122)'
    assert Original(*params).as_api_input() == expected

    params = ['US08/921,321']
    expected = '(US08/921%2C321)'
    assert Original(*params).as_api_input() == expected

    params = ['US08/921,321', None, 'B2', '20140122']
    expected = '(US08/921%2C321).(B2).(20140122)'
    assert Original(*params).as_api_input() == expected


def test_docdb_as_api_input():
    params = ['US08/921,321', 'CC', 'B2', '20140122']
    expected = '(CC).(US08/921%2C321).(B2).(20140122)'
    assert Docdb(*params).as_api_input() == expected


def test_epodoc_as_api_input():
    params = ['US08/921,321', 'B2', '20140122']
    assert Epodoc(*params).as_api_input() == '(US08/921%2C321).(B2).(20140122)'

    params = ['US08/921,321', '', '20140122']
    assert Epodoc(*params).as_api_input() == '(US08/921%2C321).(20140122)'


# TODO: Test token expiration


if __name__ == '__main__':
    pytest.main()
