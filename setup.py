#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
from os import path

from setuptools import setup
from versioningit import get_cmdclasses

if sys.argv[-1] == "publish":
    # FIXME: S605 Starting a process with a shell: seems safe, but may be changed in the future; consider rewriting without `shell`
    # FIXME: S607 Starting a process with a partial executable path
    os.system("python setup.py sdist upload")  # noqa: S605, S607
    sys.exit()

packages = ["epo_ops"]

requires = [
    "dogpile.cache<1.2",
    "importlib-metadata; python_version<'3.8'",
    "python-dateutil<2.9",
    "requests>=2.27,<3",
    "six<2",
]
extras = {
    "develop": [
        "black<24",
        "ruff==0.0.285; python_version >= '3.7'",
        "twine<5",
        "wheel<1",
    ],
    "test": [
        "pytest<8",
        "pytest-cache<2",
        "pytest-cov<4.2",
        "python-dotenv<0.20",
        "responses<0.24",
    ],
}

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="python-epo-ops-client",
    cmdclass=get_cmdclasses(),
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
    download_url="https://pypi.org/project/python-epo-ops-client/#files",
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
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
    ],
)
