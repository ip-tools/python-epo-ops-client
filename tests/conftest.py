import pytest

from secrets import KEY, SECRET
from helpers import mkcache, mksqlite, mkthrottler


@pytest.fixture
def storage(request):
    return mksqlite(request)


@pytest.fixture
def reset_cached_client(request):
    from epo_ops import Client
    return Client(middlewares=[mkcache(request), mkthrottler(request)])


@pytest.fixture
def reset_cached_registered_client(request):
    from epo_ops import RegisteredClient
    return RegisteredClient(
        KEY, SECRET, middlewares=[mkcache(request), mkthrottler(request)]
    )


@pytest.fixture(
    params=['reset_cached_client', 'reset_cached_registered_client']
)
def reset_cached_clients(request):
    return request.getfuncargvalue(request.param)


@pytest.fixture(scope='module')
def module_cache(request):
    return mkcache(request)


@pytest.fixture(scope='module')
def default_client(request):
    from epo_ops import Client
    return Client(middlewares=[mkthrottler(request)])


@pytest.fixture(scope='module')
def cached_client(request, module_cache):
    from epo_ops import Client
    return Client(middlewares=[module_cache, mkthrottler(request)])


@pytest.fixture(scope='module')
def default_registered_client(request):
    from epo_ops import RegisteredClient
    return RegisteredClient(KEY, SECRET, middlewares=[mkthrottler(request)])


@pytest.fixture(scope='module')
def cached_registered_client(request, module_cache):
    from epo_ops import RegisteredClient
    return RegisteredClient(
        KEY, SECRET, middlewares=[module_cache, mkthrottler(request)]
    )


@pytest.fixture(
    scope='module',
    params=['default_registered_client', 'cached_registered_client']
)
def registered_clients(request):
    return request.getfuncargvalue(request.param)


@pytest.fixture(
    scope='module',
    params=['cached_client', 'cached_registered_client']
)
def cached_clients(request):
    return request.getfuncargvalue(request.param)


@pytest.fixture(
    scope='module',
    params=[
        'default_client', 'cached_client', 'default_registered_client',
        'cached_registered_client'
    ]
)
def all_clients(request):
    return request.getfuncargvalue(request.param)
