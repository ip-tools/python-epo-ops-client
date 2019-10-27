import pytest

from .helpers import mkcache, mksqlite, mkthrottler
from .secrets import OPS_KEY, OPS_SECRET


@pytest.fixture
def storage(request):
    return mksqlite(request)


@pytest.fixture
def reset_cached_client(request):
    from epo_ops import Client

    return Client(
        OPS_KEY, OPS_SECRET, middlewares=[mkcache(request), mkthrottler(request)]
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

    return Client(OPS_KEY, OPS_SECRET, middlewares=[mkthrottler(request)])


@pytest.fixture(scope="module")
def cached_client(request, module_cache):
    from epo_ops import Client

    return Client(OPS_KEY, OPS_SECRET, middlewares=[module_cache, mkthrottler(request)])


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
