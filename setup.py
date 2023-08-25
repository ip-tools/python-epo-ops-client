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

requires = [
    "dogpile.cache<1.2",
    "python-dateutil<2.9",
    "requests>=2.27,<3",
    "six<2",
]
extras = {
    "develop": [
        "black<24",
        "bump2version<1.1",
        "flake8<6",
        "flake8-bugbear<22",
        "isort<6",
        "seed-isort-config<3",
        "twine<5",
        "wheel<1",
    ],
    "test": [
        "pytest<8",
        "pytest-cache<2",
        "pytest-cov<4.2",
        "python-dotenv<0.20",
    ],
}

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="python-epo-ops-client",
    version=__version__,
    description=(
        "Python client for EPO OPS, "
        "the European Patent Office's Open Patent Services API."
    ),
    long_description_content_type="text/markdown",
    long_description=readme,
    author="George Song",
    author_email="george@monozuku.com",
    maintainer="Andreas Motl",
    maintainer_email="andreas.motl@ip-tools.org",
    url="https://github.com/ip-tools/python-epo-ops-client",
    download_url=(
        "https://github.com/ip-tools/python-epo-ops-client/archive/"
        "v%s.tar.gz" % __version__
    ),
    packages=packages,
    package_dir={"epo_ops": "epo_ops"},
    include_package_data=True,
    install_requires=requires,
    extras_require=extras,
    tests_require=extras["test"],
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
    keywords=[
        "ops",
        "epo",
        "epo-ops",
        "patent-data",
        "patent-office",
        "patent-data-api",
        "european patent office",
        "open patent services",
    ]
)
