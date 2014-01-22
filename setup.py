#!/usr/bin/env python

import os
import sys

import epo_ops

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'epo_ops',
]

requires = []

with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='python-epo-ops-client',
    version=epo_ops.__version__,
    description='Python client for EPO OPS.',
    long_description=readme + '\n\n' + history,
    author='George Song',
    author_email='george@55minutes.com',
    url='http://python-requests.org',  # TODO: URL
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'epo_ops': 'epo_ops'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(  # TODO: Get the right classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)
