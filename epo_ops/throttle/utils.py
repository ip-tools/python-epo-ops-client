import re
import logging

log = logging.getLogger(__name__)


def service_for_url(url):
    urlpatterns = {
        '/published-data/search': 'search',
        '/published-data/images': 'images',
        '/published-data': 'retrieval',
        '/family': 'inpadoc',
        '/legal': 'inpadoc',
        '/classification/cpc/media': 'images',
    }

    for pattern, service in urlpatterns.items():
        if re.search('rest-services{}'.format(pattern), url):
            return service

    return 'other'
