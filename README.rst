python-epo-ops-client
=====================

|PyPI version| |Build Status| |Coverage Status|

python-epo-ops-client is an `Apache2 Licensed`_ client library for
accessing the `European Patent Office`_\ ’s (“EPO”) `Open Patent
Services`_ (“OPS”) v.3.2 (based on `v 1.3.4 of the reference guide`_).

.. code:: python

    import epo_ops

    client = epo_ops.Client(key='abc', secret='xyz')  # Instantiate client
    response = client.published_data(  # Retrieve bibliography data
      reference_type = 'publication',  # publication, application, priority
      input = epo_ops.models.Docdb('1000000', 'EP', 'A1'),  # original, docdb, epodoc
      endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
      constituents = []  # optional, list of constituents
    )

--------------

Features
--------

python_epo_ops_client abstracts away the complexities of accessing EPO
OPS:

-  Format the requests properly
-  Bubble up quota problems as proper HTTP errors
-  Handle token authentication and renewals automatically
-  Handle throttling properly
-  Add optional caching to minimize impact on the OPS servers

There are two main layers to python_epo_ops_client: Client and
Middleware.

Client
~~~~~~

The Client contains all the formatting and token handling logic and is
what you’ll interact with mostly.

When you issue a request, the response is a `requests.Response`_ object.
If ``response.status_code != 200`` then a ``requests.HTTPError``
exception will be raised — it’s your responsibility to handle those
exceptions if you want to. The one case that’s handled is when the
access token has expired: in this case, the client will automatically
handle the HTTP 400 status and renew the token.

Note that the Client does not attempt to interpret the data supplied by
OPS, so it’s your responsibility to parse the XML or JSON payload for
your own purpose.

The following custom exceptions are raised for cases when OPS quotas are
exceeded, they are all in the ``epo_ops.exceptions`` module and are
subclasses of ``requests.HTTPError``, and therefore offer the same
behaviors:

-  IndividualQuotaPerHourExceeded
-  RegisteredQuotaPerWeekExceeded

Again, it’s up to you to parse the response and decide what to do.

Currently the Client knows how to issue request for the following
services:

+---------------------------------------------------+-----------------------+-----------+
| Client method                                     | API end point         | throttle  |
|                                                   |                       |           |
+===================================================+=======================+===========+
| ``family(reference_type, input, endpoint=None,    | family                | inpadoc   |
| constituents=None)``                              |                       |           |
+---------------------------------------------------+-----------------------+-----------+
| ``image(path, range=1, extension='tiff')``        | published-data/images | other     |
+---------------------------------------------------+-----------------------+-----------+
| ``number(reference_type, input, output_format)``  | number-service        | other     |
+---------------------------------------------------+-----------------------+-----------+
| ``published_data(reference_type, input,           | published-data        | retrieval |
| endpoint='biblio', constituents=None)``           |                       |           |
+---------------------------------------------------+-----------------------+-----------+
| ``published_data_search(cql, range_begin=1,       | published-data/search | search    |
| range_end=25, constituents=None)``                |                       |           |
+---------------------------------------------------+-----------------------+-----------+
| ``register(reference_type, input,                 | register              | other     |
| constituents=['biblio'])``                        |                       |           |
+---------------------------------------------------+-----------------------+-----------+
| ``register_search(cql, range_begin=1,             | register/search       | other     |
| range_end=25)``                                   |                       |           |
+---------------------------------------------------+-----------------------+-----------+
| ``register_search(cql, range_begin=1,             | register/search       | other     |
| range_end=25)``                                   |                       |           |
+---------------------------------------------------+-----------------------+-----------+

See the `OPS guide`_ or use the `Developer’s Area`_ for more information
on how to use each service.

Please submit pull requests for the following services by enhancing the
``epo_ops.api.Client`` class:

-  Legal service
-  Bulk operations

Middleware
~~~~~~~~~~

All requests and responses are passed through each middleware object
listed in ``client.middlewares``. Requests are processed in the order
listed, and responses are processed in the *reverse* order.

Each middleware should subclass ``middlewares.Middleware`` and implement
the ``process_request`` and ``process_response`` methods.

There are two middleware classes out of the box: Throttler and Dogpile.
Throttler is in charge of the OPS throttling rules and will delay
requests accordingly. Dogpile is an optional cache which will cache all
HTTP status 200, 404, 405, and 413 responses.

By default, only the Throttler middleware is enabled, if you want to
enable caching:

.. code:: python

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

*Note that caching middleware should be first in most cases.*

Dogpile
^^^^^^^

Dogpile is based on (surprise) `dogpile.cache`_. By default it is
instantiated with a DBMBackend region with timeout of 2 weeks.

Dogpile takes three optional instantiation parameters:

-  ``region``: You can pass whatever valid `dogpile.cache Region`_ you
   want to backend the cache
-  ``kwargs_handlers``: A list of keyword argument handlers, which it
   will use to process the kwargs passed to the request object in order
   to extract elements for generating the cache key. Currently one
   handler is implemented (and instantiated by default) to make sure
   that the range request header is part of the cache key.
-  ``http_status_codes``: A list of HTTP status codes that you would
   like to have cached. By default 200, 404, 405, and 413 responses are
   cached.

**Note**: dogpile.cache is not installed by default, if you want to use
it, ``pip install dogpile.cache`` in your project.

Throttler
^^^^^^^^^

Throttler contains all the logic for handling different throttling
scenarios. Since OPS throttling is based on a one minute rolling window,
we must persist historical (at least for the past minute) throtting data
in order to know what the proper request frequency is. Each Throttler
must be instantiated with a Storage object.

Storage
'''''''

The Storage object is responsible for:

1. Knowing how to update the historical record with each request
   (``Storage.update()``), making sure to observe the one minute rolling
   window rule.
2. Calculating how long to wait before issuing the next request
   (``Storage.delay_for()``).

Currently the only Storage backend provided is SQLite, but you can
easily write your own Storage backend (such as file, Redis, etc.). To
use a custom Storage type, just pass the Storage object when you’re
instantiating a Throttler object. See
``epo_ops.middlewares.throttle.storages.Storage`` for more
implementation details.

--------------

Tests
-----

Tests are written using `pytest`_. To run the tests:

1. `Register a OPS user login with EPO`_
2. Create an app
3. Look up the Mock Server URL at `Apiary`_
4. Set the ``APIARY_URL``, ``OPS_KEY``, and ``OPS_SECRET`` environment
   variables accordingly
5. ``make test``

The tests must be run with a working internet connection, since both OPS
and the `mock Apiary services`_ are online.

.. _Apache2 Licensed: http://www.apache.org/licenses/LICENSE-2.0
.. _European Patent Office: http://epo.org
.. _Open Patent Services: http://www.epo.org/searching/free/ops.html
.. _v 1.3.4 of the reference guide: http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$FILE/ops_v3.2_documentation%20_version_1.3.4_en.pdf
.. _requests.Response: http://requests.readthedocs.org/en/latest/user/advanced/#request-and-response-objects
.. _OPS guide: http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$FILE/ops_v3.2_documentation%20_version_1.3.4_en.pdf
.. _Developer’s Area: https://developers.epo.org/ops-v3-2/apis
.. _dogpile.cache: https://bitbucket.org/zzzeek/dogpile.cache
.. _dogpile.cache Region: http://dogpilecache.readthedocs.org/en/latest/api.html#module-dogpile.cache.region
.. _pytest: http://pytest.org/latest/
.. _Register a OPS user login with EPO: https://developers.epo.org/user/register
.. _Apiary: http://docs.opsv31.apiary.io
.. _mock Apiary services: http://docs.opsv31.apiary.io

.. |PyPI version| image:: http://img.shields.io/pypi/v/python-epo-ops-client.svg
   :target: https://pypi.python.org/pypi/python-epo-ops-client
.. |Build Status| image:: http://img.shields.io/travis/55minutes/python-epo-ops-client.svg
   :target: https://travis-ci.org/55minutes/python-epo-ops-client
.. |Coverage Status| image:: http://img.shields.io/coveralls/55minutes/python-epo-ops-client.svg
   :target: https://coveralls.io/r/55minutes/python-epo-ops-client
