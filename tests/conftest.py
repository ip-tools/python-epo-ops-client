import pytest

from .helpers import mkcache, mksqlite, mkthrottler
from .secrets import get_secrets_or_skip_tests


@pytest.fixture
def storage(request):
    return mksqlite(request)


@pytest.fixture
def reset_cached_client(request):
    from epo_ops import Client

    ops_key, ops_secret = get_secrets_or_skip_tests()
    return Client(
        ops_key, ops_secret, middlewares=[mkcache(request), mkthrottler(request)]
    )


@pytest.fixture(params=["reset_cached_client"])
def reset_cached_clients(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="module")
def module_cache(request):
    return mkcache(request)


@pytest.fixture(scope="module")
def default_client(request):
    from epo_ops import Client

    ops_key, ops_secret = get_secrets_or_skip_tests()

    return Client(ops_key, ops_secret, middlewares=[mkthrottler(request)])


@pytest.fixture(scope="module")
def cached_client(request, module_cache):
    from epo_ops import Client

    ops_key, ops_secret = get_secrets_or_skip_tests()

    return Client(ops_key, ops_secret, middlewares=[module_cache, mkthrottler(request)])


@pytest.fixture(scope="module", params=["cached_client", "default_client"])
def clients(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="module", params=["default_client"])
def non_cached_clients(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="module", params=["cached_client"])
def cached_clients(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="module", params=["cached_client", "default_client"])
def all_clients(request):
    return request.getfixturevalue(request.param)
