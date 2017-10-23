#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import sys

from __version__ import __version__


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'epo_ops',
]

requires = ['python-dateutil', 'requests', 'six']

readme = open('README.rst').read()
history = open('HISTORY.rst').read()
license = open('LICENSE').read()

setup(
    name='python-epo-ops-client',
    version=__version__,
    description=(
        "Python Client for the European Patent Office's "
        "Open Patent Services API"
    ),
    long_description=readme + '\n\n' + history,
    author='George Song',
    author_email='george@monozuku.com',
    url='https://github.com/55minutes/python-epo-ops-client',
    download_url=(
        'https://github.com/55minutes/python-epo-ops-client/archive/'
        'v%s.tar.gz' % __version__
    ),
    packages=packages,
    package_dir={'epo_ops': 'epo_ops'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    tests_require=['pytest', 'pytest-cache', 'pytest-cov'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
