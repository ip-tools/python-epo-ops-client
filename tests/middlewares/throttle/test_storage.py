import pytest

from epo_ops.middlewares.throttle.storages import Storage


def test_storage_base_class_not_implemented():
    s = Storage()
    for m in (s.delay_for, s.update):
        with pytest.raises(NotImplementedError):
            m("something")
