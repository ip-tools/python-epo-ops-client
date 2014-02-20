import pytest

from epo_ops.middlewares.cache.dogpile import Dogpile, dogpile


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


if __name__ == '__main__':
    pytest.main()
