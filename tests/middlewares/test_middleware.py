import pytest

from epo_ops.middlewares.middleware import Middleware


def test_storage_base_class_not_implemented():
    o = Middleware()
    for m in (o.process_request, o.process_response):
        with pytest.raises(NotImplementedError):
            m('something')


if __name__ == '__main__':
    pytest.main()
