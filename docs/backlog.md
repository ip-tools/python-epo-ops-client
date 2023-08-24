# Backlog


## Iteration +1

- Use new organization name `ip-tools`
- Dissolve `requirements` files, and inline them into `setup.py`
- CI: Add GHA recipe, dissolve Travis configuration
- Use `ruff` linter, dissolve `flake8` and `isort`
- Use `versioningit` for versioning, dissolve `bumpversion`
- Switch to `pyproject.toml`
- Setup project documentation on Read the Docs


## Iteration +2

This is the content of the original `TODOS.md` file.

- Feature: Should the non-standard oAuth be coded as a requests plug-in?
- Dogpile caching
  - Generate the key based on a SortedDict of some kind to make sure the exact
    same request with different argument order are still a hit
- Testing: Replace Apiary tests with monkeypatch? Or
  <https://pypi.python.org/pypi/pytest-localserver>.
- Additional services
  - Legal service
- Makefile: Comma in `echo` statements?
