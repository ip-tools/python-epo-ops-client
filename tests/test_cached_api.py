import pytest


@pytest.fixture
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.session.Session.request")


def test_something():
    pass


if __name__ == '__main__':
    pytest.main()
