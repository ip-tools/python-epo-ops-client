# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from os.path import abspath, dirname, join
import os

from dotenv import load_dotenv

dotenv_path = abspath(join(dirname(__file__), '../.env'))
load_dotenv(dotenv_path)

APIARY_URL = os.environ['APIARY_URL']
KEY = os.environ['OPS_KEY']
SECRET = os.environ['OPS_SECRET']
