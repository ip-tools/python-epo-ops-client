# Backlog


## Iteration +1

- Improve and clean up README
- Set up project documentation on Read the Docs
- Switch to `pyproject.toml`


## Iteration +2

This is the content of the original `TODOS.md` file.

- Feature: Should the non-standard oAuth be coded as a requests plug-in?
- Dogpile caching
  - Generate the key based on a SortedDict of some kind to make sure the exact
    same request with different argument order are still a hit
- Additional services
  - Legal service
- Makefile: Comma in `echo` statements?


## Done

- Use new organization name `ip-tools`
- CI: Add GHA recipe, dissolve Travis configuration
- Dissolve `requirements` files, and inline them into `setup.py`
- Add support for Python 3.10 and 3.11
- Use `ruff` linter, dissolve `flake8` and `isort`
- Use `versioningit` for versioning, dissolve `bumpversion`
- Replace Apiary Mock server
  https://github.com/ip-tools/python-epo-ops-client/issues/65
- Testing: Replace Apiary tests with monkeypatch? Or
  <https://pypi.python.org/pypi/pytest-localserver>.
