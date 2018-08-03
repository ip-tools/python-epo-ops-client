from .middlewares import *

INSTALLED_MIDDLEWARE = {
    "throttler": Throttler(),
    "json_response": JsonResponse(),
}


