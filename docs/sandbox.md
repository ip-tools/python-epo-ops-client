# Development Sandbox

Ready to contribute? This page describes how to set up `python-epo-ops-client`
for local development.

In order to learn how to fork the project, and submit changes back to mainline
on behalf of a pull request, see the [contributing guidelines](contributing.md).


## Sandbox Setup

1.  Acquire sources:
    ```shell
    git clone https://github.com/ip-tools/python-epo-ops-client
    cd python-epo-ops-client/
    ```

2.  Install your local copy into a Python virtualenv, in order to isolate
    it from your system Python.
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install required Python packages.
    ```shell
    pip install -r requirements/dev.txt
    ```


## OPS Account Setup

Running the software tests require a working OPS account.

1.  [Register a OPS user login with EPO][ops registration]
2.  Create an app
3.  Look up the Mock Server URL at [Apiary][apiary ops], or try
    <http://private-anon-111333769e-opsv31.apiary-mock.com>.
4.  Set the `APIARY_URL`, `OPS_KEY`, and `OPS_SECRET` environment variables
    accordingly in a `.env` file (see `example.env`).


## Software Tests

### Basics

```shell
make test
tox -e lint
tox
```

⚠️ Note that the software tests need a working internet connection, in order to
access both the OPS and the [OPS Apiary Mock Services][apiary ops] services.

⚠️ Note that the `lint` testenv requires python3.8 to be present in your
system.


### Advanced Usage

To focus on specific parts of the code base, you run a subset of the software
tests.

Run all tests in a specific module.
```shell
pytest tests/test_utils.py
```

Run all tests containing "api".
```shell
pytest -k api
```

To run `tox` for a specific Python version:
```shell
tox -e py27
```


[apiary ops]: http://docs.opsv31.apiary.io
[ops registration]: https://developers.epo.org/user/register
