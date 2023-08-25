from pytest import raises

from epo_ops.exceptions import InvalidDate
from epo_ops.utils import quote, validate_date


def test_encoding():
    # See OPS documentation, Input construction encoding rule
    assert quote('/\\?@#%$&+,:;= "<>{}|^~[]`') == (
        "/\\%3F%40%23%25%24%26%2B%2C%3A%3B%3D%20%22%3C%3E%7B%7D%7C%5E%7E%5B%5D%60"
    )


def test_valid_date():
    # Dates are YYYYMMDD
    assert validate_date("19940101") == "19940101"


def test_invalid_date():
    with raises(InvalidDate):
        validate_date("abc")
    with raises(InvalidDate):
        validate_date("19941301")
