# python-epo-ops-client TODOs

## Features
* Should the non-standard oAuth be coded as a requests plug-in?

## Dogpile caching
* Generate the key based on a SortedDict of some kind to make sure the exact
  same request with different argument order are still a hit

## Testing
* Replace Apiary tests with monkeypatch? Or
  <https://pypi.python.org/pypi/pytest-localserver>.

## Additional services
* Legal service
* Bulk operations

## Makefile
* Comma in `echo` statements?
