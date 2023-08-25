# Change Log

- Add support for Python 3.10 and 3.11
- Configure HTTP client to use a network timeout of 10 seconds
- Use `versioningit` for versioning
- Tests: Remove dependency on Apiary Mock Server API

## 4.0.0 (2021-09-19)

- Upgrade dependencies
- Drop support for Python 2.7 and Python 3.5
- Add support for Python 3.9

## 3.1.3 (2020-09-23)

- Upgrade dependencies

## 3.1.2 (2020-07-04)

- Upgrade dependencies

## 3.1.1 (2019-10-28)

- GET instead of POST for family services, thanks to [amotl][]. See
  [#33](https://github.com/ip-tools/python-epo-ops-client/issues/33) for more
  info.

## 3.1.0 (2019-10-27)

- Add support for bulk retrieval, thanks to [mmath][]

## 3.0.0 (2019-10-27)

- Drop support for PyPy, Python 3.4 (probably still works)
- Add support for Python 3.7, 3.8
- Invalid and expired tokens are now treated the same, since OPS doesn't
  distinguish between the two use cases.

## 2.3.2 (2018-01-15)

- Bug fix: Cache 4xx results as well, thanks to [amotl][]

## 2.3.1 (2017-11-10)

- Bug fix: explicitly declare content-type during request

## 2.3.0 (2017-10-22)

- Drop support for Python 2.6
- Officially support Python 3.6
- Update to latest dependencies
- Add image retrieval service, thanks to [rfaga][]

## 2.2.0 (2017-03-30)

- EPO OPS v3.2 compatibility, thanks to [eltermann][]

## 2.1.0 (2016-02-21)

- Add number service, thanks to [eltermann][]

## 2.0.0 (2015-12-11)

- Dropping support for Python 3.3 (although it probably still works).
- Update to latest dependencies, no new features.

## 1.0.0 (2015-09-20)

- Allow no middleware to be specified
- Minor tweaks to development infrastructure, no new features.
- This has been working for a while now, let's call it 1.0!

## 0.1.9 (2015-07-21)

- No new features, just updating third party dependencies

## 0.1.8 (2015-01-24)

- No new features, just updating third party dependencies

## 0.1.7 (2015-01-24)

- Created default Dogpile DBM path if it doesn't exist

## 0.1.6 (2014-12-12)

- Fixed bug with how service URL is constructed

## 0.1.5 (2014-10-17)

- Added support for register retrieval and search

## 0.1.4 (2014-10-10)

- Verified PyPy3 support
- Updated various dependency pacakges

## 0.1.3 (2014-05-21)

- Python 3.4 compatibility
- Updated `requests` dependency to 2.3.0

## 0.1.2 (2014-03-04)

- Python 2.6 and 3.3 compatibility

## 0.1.1 (2014-03-01)

- Allow configuration of which HTTP responses (based on status code) to cache

## 0.1.0 (2014-02-20)

- Introduced dogpile.cache for caching http200 resopnses
- Introduced the concept of middleware

## 0.0.1 (2014-01-21)

- Initial release

[amotl]: https://github.com/amotl
[eltermann]: https://github.com/eltermann
[mmath]: https://github.com/mmath
[rfaga]: https://github.com/rfaga
