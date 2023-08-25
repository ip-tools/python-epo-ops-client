import os
from random import shuffle

import pytest

from epo_ops.api import Client
from epo_ops.middlewares.throttle.utils import URLPATTERNS, service_for_url


@pytest.fixture
def urls():
    test_urls = [
        (os.path.join(Client.__service_url_prefix__, path, "xxx"), service)
        for path, service in URLPATTERNS + (("xxx", "other"),)
    ]
    shuffle(test_urls)
    return test_urls


def test_return_right_service_for_url(urls):
    for url, service in urls:
        assert service_for_url(url) == service
