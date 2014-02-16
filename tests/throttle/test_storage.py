import pytest

from epo_ops.throttle.storages import Storage


def test_storage_base_class_not_implemented():
    with pytest.raises(NotImplementedError):
        Storage().delay_for('something')
    with pytest.raises(NotImplementedError):
        Storage().update('something')


if __name__ == '__main__':
    pytest.main()
