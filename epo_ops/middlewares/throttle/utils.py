# -*- coding: utf-8 -*-

import logging
import re

log = logging.getLogger(__name__)

# Since patterns are searched in order, we need to specify from most to least
# specific
URLPATTERNS = (
    ("classification/cpc/media", "images"),
    ("family", "inpadoc"),
    ("legal", "inpadoc"),
    ("published-data/images", "images"),
    ("published-data/search", "search"),
    ("published-data", "retrieval"),
)


def service_for_url(url):
    for pattern, service in URLPATTERNS:
        if re.search("rest-services/{0}".format(pattern), url):
            return service

    return "other"
