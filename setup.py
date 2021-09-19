#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
from os import path

from setuptools import setup

from __version__ import __version__

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

packages = ["epo_ops"]

requires = ["python-dateutil", "requests", "six"]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open(path.join(here, "CHANGELOG.md"), encoding="utf-8") as f:
    history = f.read()

setup(
    name="python-epo-ops-client",
    version=__version__,
    description=(
        "Python Client for the European Patent Office's " "Open Patent Services API"
    ),
    long_description_content_type="text/markdown",
    long_description=u"{}\n{}".format(readme, history),
    author="George Song",
    author_email="george@monozuku.com",
    url="https://github.com/gsong/python-epo-ops-client",
    download_url=(
        "https://github.com/gsong/python-epo-ops-client/archive/"
        "v%s.tar.gz" % __version__
    ),
    packages=packages,
    package_dir={"epo_ops": "epo_ops"},
    include_package_data=True,
    install_requires=requires,
    tests_require=["pytest", "pytest-cache", "pytest-cov"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
