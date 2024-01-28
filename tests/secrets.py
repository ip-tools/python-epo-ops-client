# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
from os.path import abspath, dirname, join

import pytest
from dotenv import load_dotenv

# Prune environment variables.
for k in ("OPS_KEY", "OPS_SECRET"):
    if k in os.environ and not os.environ[k]:
        del os.environ[k]

# Load environment variables from `.env` file.
dotenv_path = abspath(join(dirname(__file__), "../.env"))
load_dotenv(dotenv_path)


# Set environment variables as constants.
def get_secrets_or_skip_tests():
    try:
        ops_key = os.environ["OPS_KEY"]
        ops_secret = os.environ["OPS_SECRET"]
    except KeyError as ex:
        raise pytest.skip("No OPS credentials configured") from ex

    return ops_key, ops_secret
