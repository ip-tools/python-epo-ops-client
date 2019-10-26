import pytest

from epo_ops.middlewares.middleware import Middleware


def test_storage_base_class_not_implemented():
    o = Middleware()
    with pytest.raises(NotImplementedError):
        o.process_request(*["x"] * 3)
    with pytest.raises(NotImplementedError):
        o.process_response(*["x"] * 2)


if __name__ == "__main__":
    pytest.main()
