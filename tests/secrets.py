# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os.path import abspath, dirname, join

from dotenv import load_dotenv

# Workaround tox environment issue, where these keys would be set to empty
for k in ("APIARY_URL", "OPS_KEY", "OPS_SECRET"):
    if k in os.environ and not os.environ[k]:
        del os.environ[k]

dotenv_path = abspath(join(dirname(__file__), "../.env"))
load_dotenv(dotenv_path)

APIARY_URL = os.environ["APIARY_URL"]
OPS_KEY = os.environ["OPS_KEY"]
OPS_SECRET = os.environ["OPS_SECRET"]
