.DEFAULT_GOAL := help
.PHONY: clean-build clean-pyc install-virtualenv-hooks

PWD = $(shell pwd)

define bold-yellow-echo
	@tput bold
	@tput setaf 3
	@echo $1
	@tput sgr0
endef

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message
	@echo "Please use \`make <target>' where <target> is one of the following:"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

seed-isort-config: ## Update known third party dependencies
	seed-isort-config --application-directories .:epo_ops --exclude setup.py

pip-compile: ## Update compiled requirement files
	bin/pip-compile.sh

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## flake8 lint the project
	flake8 epo_ops tests

test: clean ## Run tests with virtualenv Python
	py.test -s -v --lf --cov-report term --cov epo_ops tests

test-ci: clean ## Run tests in CI environment with virtualenv Python
	py.test -v --cov epo_ops --cov-report term-missing

tox: clean ## Run tests with all supported Python versions
	tox

coverage: clean ## Check code coverage locally
	py.test -s -v --cov-report html --cov-report term --cov epo_ops tests
	open htmlcov/index.html

release: clean # Package and upload a release to PyPI
	python setup.py sdist
	python setup.py bdist_wheel
	twine check dist/*
	twine upload --repository pypi dist/*
	open https://pypi.python.org/pypi/python-epo-ops-client

release-test: clean # Package and upload a release to testpypi
	python setup.py sdist
	python setup.py bdist_wheel
	twine check dist/*
	twine upload --repository test dist/*
	open https://testpypi.python.org/pypi/python-epo-ops-client

sdist: clean
	python setup.py sdist
	ls -l dist
