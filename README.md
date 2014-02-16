python-epo-ops-client
=====================

python-epo-ops-client is an Apache2 Licensed client library for accessing the
[European Patent Office][EPO]'s ("EPO") [Open Patent Services][OPS] ("OPS")
v.3.1 (based on [v 1.2.10 of the reference guide][refguide]).

```
import epo_ops

anonymous_client = epo_ops.Client()
response = anonymous_client.published_data(
  reference_type = 'publication',  # publication, application, priority
  input = epo_ops.Docdb('1000000', 'EP', 'A1'),  # original, docdb, epodoc
  endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
  constituents = []  # optional, array of optional constituents
)

client = epo_ops.RegisteredClient(key='abc', secret='xyz')
client.access_token  # To see the current token
response = client.published_data(…)
```

## Features

python_epo_ops_client abstracts away the complexities of access EPO OPS:

* Formatting the requests properly
* Bubbling up quota problems as proper HTTP errors
* Handle token authentication and renewals automatically
* Handle throttling properly

There are three main layers to python_epo_ops_client: Client, Throttler, and
Storage.

### Client

The Client contains all the formatting and token handling logic and issues the
requests using Throttler. The Client class is what you'll interact with mostly.

### Throttler

Throttler is just a thin wrapper around the [requests][] package. It contains
all the logic handling different throttling scenarios. Since OPS throttling is
based on a one minute rolling window, we must store historical (at least for
the past minute) throtting controls in order to know what the proper request
frequency is. Each Throttler must be instantiated with a Storage object.

### Storage

The Storage object is responsible for knowing how to update the historical
record with each request, making sure to observe the one minute rolling window
rule, and be able to calculate how long to wait before issuing the next
request.

Currently the only Storage type provided is SQLite, but you can easily write
your own Storage type (such as file, Redis, etc.). Just pass the Storage object
when you're instantiating a Client object. See
`epo_ops.throttle.storages.Storage` for more implementation details.

---

`response` is a [`requests.Response`][requests.Response] object. If
`response.status_code != 200` then an exception will be raised, it's your
responsibility to handle those exceptions if you want to. The one case that's
handled by the RegisteredClient is when its access token has expired, in this
case, the client will automatically handle the HTTP 400 status and renew the
token.

The following custom exceptions are raised for cases when OPS quotas are
exceeded, they are all subclasses of `requests.HTTPError` and offer the same
behavior:

* AnonymousQuotaPerMinuteExceeded
* AnonymousQuotaPerDayExceeded
* IndividualQuotaPerHourExceeded
* RegisteredQuotaPerWeekExceeded

## Tests

Tests are written using pytest. To run the tests:

1.  Register a OPS user login with EPO
2.  Create an app
3.  Record the app's consumer key and secret in `tests/secrets.py` (see
    `secrets.py.example`)
4.  `py.test -s --cov-report html --cov-report term --cov epo_ops tests`

The tests must be run with a working internet connection, since both OPS and
the mock Apiary services are online.


[EPO]: http://epo.org
[OPS]: http://www.epo.org/searching/free/ops.html
[refguide]: http://documents.epo.org/projects/babylon/eponet.nsf/0/7AF8F1D2B36F3056C1257C04002E0AD6/$File/OPS_RWS_ReferenceGuide_version1210_EN.pdf
[requests]: http://requests.readthedocs.org/en/latest/
[requests.Response]: http://requests.readthedocs.org/en/latest/user/advanced/#request-and-response-objects
