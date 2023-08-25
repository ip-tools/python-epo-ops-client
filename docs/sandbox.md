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

3.  Install required Python packages into development sandbox.
    ```shell
    make install-develop
    ```


## Software Tests


### OPS Account Setup

Running the software tests require a working OPS account.

1.  [Sign up for an OPS user login with EPO][ops registration].
2.  Create an App at the OPS Console, which will provide you with a corresponding
    pair of authentication credentials, the OPS application key and its secret.


### Prerequisites

Before running the software tests, you will need to define the
`OPS_KEY`, and `OPS_SECRET` environment variables.

You can either define them interactively using `export VARNAME=VALUE`, or store
them into an `.env` file within the same directory you are running the tests from.
See `example.env` for a blueprint.

```shell
export OPS_KEY=NKdGMmedZBGLRxTrUwCZMQCYp7Ak5a0u
export OPS_SECRET=v3vARPu7DFPEDB8i
```

_Note that the OPS credentials have been invalidated for demonstration purposes._


### Basics

```shell
make check
```

⚠️ Note that the software tests need a working internet connection, in order to
access the OPS service.


### Advanced Usage

In order to run either the linter, or the software tests exclusively,
use `make lint` vs. `make test`.

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


[ops registration]: https://developers.epo.org/user/register
