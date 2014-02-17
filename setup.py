#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import shlex
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


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = shlex.split(
            '--cov-report html --cov-report term --cov epo_ops tests'
        )
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

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
    package_data={'': ['LICENSE']},
    package_dir={'epo_ops': 'epo_ops'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',

    ),
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
)
