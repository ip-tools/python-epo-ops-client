from ..middleware import Middleware
import xmltodict
import json

def xml_json(response):
    return json.dumps(xmltodict.parse(response.text))

class JsonResponse(Middleware):
    def __init__(self):
        pass
    def process_request(self, env, url, data, **kwargs):
        return url, data, kwargs

    def process_response(self, env, response):
        response.json = xml_json
        return response
