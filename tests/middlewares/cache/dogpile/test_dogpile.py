import pytest

from epo_ops.middlewares.cache.dogpile import Dogpile, dogpile
from epo_ops.models import Request


class Response(object):
    def __init__(self, status_code):
        self.status_code = status_code


def test_default_instantiation():
    d = Dogpile()
    assert d.region.backend.filename == dogpile.DEFAULT_DBM_PATH


def test_generate_key(module_cache):
    assert module_cache.generate_key('a', 'b', x='y') == 'a|b'
    assert module_cache.generate_key('a', 'b', data='y') == 'a|b|data=y'
    assert module_cache.generate_key('a', 'b', headers={'X-OPS-Range': 5}) ==\
        'a|b|headers.X-OPS-Range=5'
    assert module_cache.generate_key(
        'a', 'b', headers={'X-OPS-Range': 5}, data='y', x='x'
    ) == 'a|b|data=y|headers.X-OPS-Range=5'


def test_process_request_and_response(module_cache):
    env = Request([]).default_env
    url = 'x'
    data = 'y'
    response = Response(200)
    response._secret = 'me'
    key = module_cache.generate_key(url, data)

    # First process, nothing in cache
    module_cache.process_request(env, url, data)
    assert env['cache-key'] == key
    assert env['from-cache'] is False
    assert env['is-cached'] is False
    assert env['response'] is None

    # Let's set the cache
    module_cache.process_response(env, response)
    assert env['cache-key'] == key
    assert env['from-cache'] is False
    assert env['is-cached'] is True
    assert module_cache.region.get(key)._secret == response._secret

    # Reset the env (just like models.Request would do)
    env = Request([]).default_env

    # Now we should have cache
    module_cache.process_request(env, url, data)
    assert env['cache-key'] == key
    assert env['from-cache'] is True
    assert env['is-cached'] is False
    assert env['response']._secret == response._secret

    # Cached shouldn't be set
    module_cache.process_response(env, response)
    assert env['cache-key'] == key
    assert env['from-cache'] is True
    assert env['is-cached'] is False
    assert env['response']._secret == response._secret


if __name__ == '__main__':
    pytest.main()
