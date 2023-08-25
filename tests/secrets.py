# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
from os.path import abspath, dirname, join

from dotenv import load_dotenv

# Prune environment variables.
for k in ("OPS_KEY", "OPS_SECRET"):
    if k in os.environ and not os.environ[k]:
        del os.environ[k]

# Load environment variables from `.env` file.
dotenv_path = abspath(join(dirname(__file__), "../.env"))
load_dotenv(dotenv_path)

# Set environment variables as constants.
OPS_KEY = os.environ["OPS_KEY"]
OPS_SECRET = os.environ["OPS_SECRET"]
