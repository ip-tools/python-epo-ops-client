#!/usr/bin/env python

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

requires = ['python-dateutil', 'requests']

with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()


setup(
    name='python-epo-ops-client',
    version=__version__,
    description=(
        "Python Client for the European Patent Office's "
        "Open Patent Services API"
    ),
    long_description=readme + '\n\n' + history,
    author='George Song',
    author_email='george@55minutes.com',
    url='https://github.com/55minutes/python-epo-ops-client',
    download_url=(
        'https://github.com/55minutes/python-epo-ops-client/archive/'
        'v{}.tar.gz'.format(__version__)
    ),
    packages=packages,
    package_dir={'epo_ops': 'epo_ops'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    tests_require=['pytest'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
