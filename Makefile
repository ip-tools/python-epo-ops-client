.PHONY: clean-pyc clean-build

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "release-test - package and upload a release to testpypi"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 --ignore=F401 epo_ops tests

test:
	py.test -s -v --lf --cov-report term --cov epo_ops tests

test-all:
	tox

coverage:
	py.test -s -v --cov-report html --cov-report term --cov epo_ops tests
	open htmlcov/index.html

release: clean
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload -r pypi
	open https://pypi.python.org/pypi/python-epo-ops-client

release-test: clean
	python setup.py sdist upload -r test
	python setup.py bdist_wheel upload -r test
	open https://testpypi.python.org/pypi/python-epo-ops-client

sdist: clean
	python setup.py sdist
	ls -l dist
