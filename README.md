python-epo-ops-client
=====================

python-epo-ops-client is an Apache2 Licensed client library for accessing the
[European Patent Office][EPO]'s ("EPO") [Open Patent Services][OPS] ("OPS")
v.3.1 (based on v 1.2.10 of the reference guide).

```
import epo_ops

anonymous_client = epo_ops.Client()
response = anonymous_client.published_data(
  reference_type = 'publication',  # publication, application, priority
  input = epo_ops.Docdb(…),  # original, docdb, epodoc
  endpoint = 'biblio', # optional, defaults to biblio in case of published_data
  constituents = [] # array of optional constituents
)


client = epo_ops.RegisteredClient(key='abc', secret='xyz')
client.access_token
response = client.published_data(…)
```

## Features

`response` is a `requests.Response` object. If `response.status_code != 200`
then an exception will be raised. The case that's handled by the
RegisteredClient is when an access token has expired, in this case, the client
will automatically handle the HTTP 400 status and renew the token.

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

