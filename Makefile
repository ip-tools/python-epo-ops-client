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

install-develop: ## Install project into sandbox.
	pip install --use-pep517 --prefer-binary --editable=.[develop,docs,test]

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

check: lint test        ## Run linter and software tests
check-ci: lint test-ci  ## Run linter and software tests on CI

lint: ## lint the project
	ruff check .
	ruff format --check .

format: ## Run code formatting
	ruff format .
	# Configure Ruff not to auto-fix (remove!):
	# Ignore unused imports (F401), unused variables (F841), `print` statements (T201), and commented-out code (ERA001).
	ruff check --fix --ignore=ERA --ignore=F401 --ignore=F841 --ignore=T20 --ignore=ERA001 .

test: clean ## Run tests with virtualenv Python
	pytest --lf

test-ci: clean ## Run tests in CI environment with virtualenv Python
	pytest

coverage: clean test-ci ## Check code coverage locally
	coverage html
	open htmlcov/index.html

release: clean # Package and upload a release to PyPI
	python -m build
	twine check dist/*
	twine upload --repository pypi dist/*
	open https://pypi.org/project/python-epo-ops-client/

release-test: clean # Package and upload a release to testpypi
	python -m build
	twine check dist/*
	twine upload --repository testpypi dist/*
	open https://test.pypi.org/project/python-epo-ops-client/

sdist: clean
	python setup.py sdist
	ls -l dist
