# python-epo-ops-client TODOs

## Features
* Should the non-standard oAuth be coded as a requests plug-in?

## Dogpile caching
* Generate the key based on a SortedDict of some kind to make sure the exact
  same request with different argument order are still a hit

## Testing
* Make sure cache is working
* Replace Apiary tests with monkeypatch?
* Travis CI

## Additional services
* Legal service
* Number service
* Register service
* Images retrieval
