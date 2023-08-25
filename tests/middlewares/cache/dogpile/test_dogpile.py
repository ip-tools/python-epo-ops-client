import pytest

import epo_ops
from epo_ops.middlewares.cache.dogpile import Dogpile, dogpile
from epo_ops.models import Request


class Response(object):
    __slots__ = ["status_code", "_secret"]

    def __init__(self, status_code):
        self.status_code = status_code


def prefix(s):
    return "epo-ops-{0}|{1}".format(epo_ops.__version__, s)


@pytest.fixture(params=[200, 404, 405, 413])
def http_status_codes(request):
    return request.param


def test_default_instantiation():
    d = Dogpile()
    assert d.region.backend.filename == dogpile.DEFAULT_DBM_PATH


def test_generate_key(module_cache):
    assert module_cache.generate_key("a", "b", x="y") == prefix("a|b")
    assert module_cache.generate_key("a", "b", headers={"X-OPS-Range": 5}) == (
        prefix("a|b|headers.X-OPS-Range=5")
    )
    assert module_cache.generate_key(
        "a", "b", headers={"X-OPS-Range": 5}, x="x"
    ) == prefix("a|b|headers.X-OPS-Range=5")


def test_process_request_and_response(module_cache, http_status_codes):
    env = Request([]).default_env
    url = "x"
    data = http_status_codes
    response = Response(http_status_codes)
    response._secret = "me"  # noqa: S105
    key = module_cache.generate_key(url, data)

    # First process, nothing in cache
    module_cache.process_request(env, url, data)
    assert env["cache-key"] == key
    assert env["from-cache"] is False
    assert env["is-cached"] is False
    assert env["response"] is None

    # Let's set the cache
    module_cache.process_response(env, response)
    assert env["cache-key"] == key
    assert env["from-cache"] is False
    assert env["is-cached"] is True
    assert module_cache.region.get(key)._secret == response._secret

    # Reset the env (just like models.Request would do)
    env = Request([]).default_env

    # Now we should have cache
    module_cache.process_request(env, url, data)
    assert env["cache-key"] == key
    assert env["from-cache"] is True
    assert env["is-cached"] is False
    assert env["response"]._secret == response._secret

    # Cached shouldn't be set
    module_cache.process_response(env, response)
    assert env["cache-key"] == key
    assert env["from-cache"] is True
    assert env["is-cached"] is False
    assert env["response"]._secret == response._secret
