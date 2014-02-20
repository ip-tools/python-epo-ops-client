# -*- coding: utf-8 -*-

from .throttle import Throttler

try:
    from .cache import Dogpile
except ImportError:  # pragma: no cover
    pass
