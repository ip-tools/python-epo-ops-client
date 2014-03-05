# -*- coding: utf-8 -*-

import logging
import re

log = logging.getLogger(__name__)

URLPATTERNS = (
    ('published-data/search', 'search'),
    ('published-data/images', 'images'),
    ('published-data', 'retrieval'),
    ('family', 'inpadoc'),
    ('legal', 'inpadoc'),
    ('classification/cpc/media', 'images'),
)


def service_for_url(url):
    for pattern, service in URLPATTERNS:
        if re.search('rest-services/{0}'.format(pattern), url):
            return service

    return 'other'
