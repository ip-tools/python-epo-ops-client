Release History
===============

2.3.1 (2017-11-10)
------------------

-  Bug fix: explicitly declare content-type during request

.. section-1:

2.3.0 (2017-10-22)
------------------

-  Drop support for Python 2.6
-  Officially support Python 3.6
-  Update to latest dependencies
-  Add image retrieval service, thanks to `rfaga`_

.. section-2:

2.2.0 (2017-03-30)
------------------

-  EPO OPS v3.2 compatibility, thanks to `eltermann`_

.. section-3:

2.1.0 (2016-02-21)
------------------

-  Add number service, thanks to `eltermann`_

.. section-4:

2.0.0 (2015-12-11)
------------------

-  Dropping support for Python 3.3 (although it probably still works).
-  Update to latest dependencies, no new features.

.. section-5:

1.0.0 (2015-09-20)
------------------

-  Allow no middleware to be specified
-  Minor tweaks to development infrastructure, no new features.
-  This has been working for a while now, let’s call it 1.0!

.. section-6:

0.1.9 (2015-07-21)
------------------

-  No new features, just updating third party dependencies

.. section-7:

0.1.8 (2015-01-24)
------------------

-  No new features, just updating third party dependencies

.. section-8:

0.1.7 (2015-01-24)
------------------

-  Created default Dogpile DBM path if it doesn’t exist

.. section-9:

0.1.6 (2014-12-12)
------------------

-  Fixed bug with how service URL is constructed

.. section-10:

0.1.5 (2014-10-17)
------------------

-  Added support for register retrieval and search

.. section-11:

0.1.4 (2014-10-10)
------------------

-  Verified PyPy3 support
-  Updated various dependency pacakges

.. section-12:

0.1.3 (2014-05-21)
------------------

-  Python 3.4 compatibility
-  Updated ``requests`` dependency to 2.3.0

.. section-13:

0.1.2 (2014-03-04)
------------------

-  Python 2.6 and 3.3 compatibility

.. section-14:

0.1.1 (2014-03-01)
------------------

-  Allow configuration of which HTTP responses (based on status code) to
   cache

.. section-15:

0.1.0 (2014-02-20)
------------------

-  Introduced dogpile.cache for caching http200 resopnses
-  Introduced the concept of middleware

.. section-16:

0.0.1 (2014-01-21)
------------------

-  Initial release

.. _rfaga: https://github.com/rfaga
.. _eltermann: https://github.com/eltermann
