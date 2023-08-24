# python-epo-ops-client

[![PyPI](https://img.shields.io/pypi/v/python-epo-ops-client)](https://pypi.org/project/python-epo-ops-client/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-epo-ops-client)](https://pypi.org/project/python-epo-ops-client/)
[![GHA](https://github.com/ip-tools/python-epo-ops-client/actions/workflows/main.yml/badge.svg)](https://github.com/ip-tools/python-epo-ops-client/actions/workflows/main.yml)
[![Codecov](https://codecov.io/gh/ip-tools/python-epo-ops-client/branch/main/graph/badge.svg)](https://codecov.io/gh/ip-tools/python-epo-ops-client)

python-epo-ops-client is an [Apache2 licensed][apache license] client library
for accessing the [European Patent Office][epo]'s ("EPO") [Open Patent
Services][ops] ("OPS") v.3.2 (based on [v 1.3.16 of the reference guide][ops guide]).

```python
import epo_ops

client = epo_ops.Client(key='abc', secret='xyz')  # Instantiate client
response = client.published_data(  # Retrieve bibliography data
  reference_type = 'publication',  # publication, application, priority
  input = epo_ops.models.Docdb('1000000', 'EP', 'A1'),  # original, docdb, epodoc
  endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
  constituents = []  # optional, list of constituents
)
```

---

## Features

`python-epo-ops-client` abstracts away the complexities of accessing EPO OPS:

- Format the requests properly
- Bubble up quota problems as proper HTTP errors
- Handle token authentication and renewals automatically
- Handle throttling properly
- Add optional caching to minimize impact on the OPS servers

There are two main layers to `python-epo-ops-client`: Client and Middleware.

### Client

The Client contains all the formatting and token handling logic and is what
you'll interact with mostly.

When you issue a request, the response is a [requests.Response][] object. If
`response.status_code != 200` then a `requests.HTTPError` exception will be
raised — it's your responsibility to handle those exceptions if you want to. The
one case that's handled is when the access token has expired: in this case, the
client will automatically handle the HTTP 400 status and renew the token.

Note that the Client does not attempt to interpret the data supplied by OPS, so
it's your responsibility to parse the XML or JSON payload for your own purpose.

The following custom exceptions are raised for cases when OPS quotas are
exceeded, they are all in the `epo_ops.exceptions` module and are subclasses of
`requests.HTTPError`, and therefore offer the same behaviors:

- IndividualQuotaPerHourExceeded
- RegisteredQuotaPerWeekExceeded

Again, it's up to you to parse the response and decide what to do.

Currently the Client knows how to issue request for the following services:

| Client method                                                                 | API end point         | throttle  |
| ----------------------------------------------------------------------------- | --------------------- | --------- |
| `family(reference_type, input, endpoint=None, constituents=None)`             | family                | inpadoc   |
| `image(path, range=1, extension='tiff')`                                      | published-data/images | images    |
| `number(reference_type, input, output_format)`                                | number-service        | other     |
| `published_data(reference_type, input, endpoint='biblio', constituents=None)` | published-data        | retrieval |
| `published_data_search(cql, range_begin=1, range_end=25, constituents=None)`  | published-data/search | search    |
| `register(reference_type, input, constituents=['biblio'])`                    | register              | other     |
| `register_search(cql, range_begin=1, range_end=25)`                           | register/search       | other     |
| `register_search(cql, range_begin=1, range_end=25)`                           | register/search       | other     |

Bulk operations can be achieved by passing a list of valid models to the
published_data input field.

See the [OPS guide][] or use the [Developer's Area][] for more information on
how to use each service.

Please submit pull requests for the following services by enhancing the
`epo_ops.api.Client` class:

- Legal service

### Middleware

All requests and responses are passed through each middleware object listed in
`client.middlewares`. Requests are processed in the order listed, and responses
are processed in the _reverse_ order.

Each middleware should subclass `middlewares.Middleware` and implement the
`process_request` and `process_response` methods.

There are two middleware classes out of the box: Throttler and Dogpile.
Throttler is in charge of the OPS throttling rules and will delay requests
accordingly. Dogpile is an optional cache which will cache all HTTP status 200,
404, 405, and 413 responses.

By default, only the Throttler middleware is enabled, if you want to enable
caching:

```python
import epo_ops

middlewares = [
    epo_ops.middlewares.Dogpile(),
    epo_ops.middlewares.Throttler(),
]
client = epo_ops.Client(
    key='key',
    secret='secret',
    middlewares=middlewares,
)
```

You'll also need to install caching dependencies in your projects, such as `pip install dogpile.cache`.

_Note that caching middleware should be first in most cases._

#### Dogpile

Dogpile is based on (surprise) [dogpile.cache][]. By default it is instantiated
with a DBMBackend region with timeout of 2 weeks.

Dogpile takes three optional instantiation parameters:

- `region`: You can pass whatever valid [dogpile.cache Region][] you want to
  backend the cache
- `kwargs_handlers`: A list of keyword argument handlers, which it will use to
  process the kwargs passed to the request object in order to extract elements
  for generating the cache key. Currently one handler is implemented (and
  instantiated by default) to make sure that the range request header is part of
  the cache key.
- `http_status_codes`: A list of HTTP status codes that you would like to have
  cached. By default 200, 404, 405, and 413 responses are cached.

**Note**: dogpile.cache is not installed by default, if you want to use it, `pip install dogpile.cache` in your project.

#### Throttler

Throttler contains all the logic for handling different throttling scenarios.
Since OPS throttling is based on a one minute rolling window, we must persist
historical (at least for the past minute) throtting data in order to know what
the proper request frequency is. Each Throttler must be instantiated with a
Storage object.

##### Storage

The Storage object is responsible for:

1.  Knowing how to update the historical record with each request
    (`Storage.update()`), making sure to observe the one minute rolling window
    rule.
2.  Calculating how long to wait before issuing the next request
    (`Storage.delay_for()`).

Currently the only Storage backend provided is SQLite, but you can easily write
your own Storage backend (such as file, Redis, etc.). To use a custom Storage
type, just pass the Storage object when you're instantiating a Throttler object.
See `epo_ops.middlewares.throttle.storages.Storage` for more implementation
details.

[apache license]: http://www.apache.org/licenses/LICENSE-2.0
[developer's area]: https://developers.epo.org/ops-v3-2/apis
[dogpile.cache region]: http://dogpilecache.readthedocs.org/en/latest/api.html#module-dogpile.cache.region
[dogpile.cache]: https://bitbucket.org/zzzeek/dogpile.cache
[epo]: http://epo.org
[ops guide]: http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.16_en.pdf
[ops]: https://www.epo.org/searching-for-patents/data/web-services/ops.html
[requests.response]: http://requests.readthedocs.org/en/latest/user/advanced/#request-and-response-objects
