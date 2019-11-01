# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways.

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/55minutes/python-epo-ops-client/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to
whoever wants to fix it.

### Implement Features

Look through TODOS.md or GitHub issues for features. Anything tagged with
"feature" is open to whoever wants to implement it.

### Write Documentation

python-epo-ops-client could always use more documentation, whether as part of
the official python-epo-ops-client docs, in docstrings, or even on the web in
blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/55minutes/python-epo-ops-client/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are
  welcome. 😊

## Get Started!

Ready to contribute? Here's how to set up `python-epo-ops-client` for local
development.

1.  Fork the `python-epo-ops-client` repo on GitHub.
2.  Clone your fork locally:

    ```
    $ git clone git@github.com:[your_name_here]/python-epo-ops-client.git
    ```

3.  Install your local copy into a virtualenv. Assuming you have
    virtualenvwrapper installed, this is how you set up your fork for local
    development:

    ```
    $ mkvirtualenv python-epo-ops-client
    $ cd python-epo-ops-client/
    $ pip install -r requirements/dev.txt
    ```

4.  Create a branch for local development:

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5.  Tests require a working OPS account

    1.  [Register a OPS user login with EPO][ops registration]
    2.  Create an app
    3.  Look up the Mock Server URL at [Apiary][apiary ops], or try
        <http://private-anon-111333769e-opsv31.apiary-mock.com>.
    4.  Set the `APIARY_URL`, `OPS_KEY`, and `OPS_SECRET` environment variables
        accordingly in a `.env` file (see `example.env`).

6.  The tests must be run with a working internet connection, since both OPS and
    the [mock Apiary services][apiary ops] are online.

7.  When you're done making changes, check that your changes pass test and
    linting, including testing other Python versions with tox. In order to run
    tox successfully, you must have all versions of Python installed on your
    machine. See `tox -a` for more details.

    ```
    $ make test
    $ tox -e lint
    $ tox
    ```

    ⚠️ Note that the `lint` testenv requries python3.8 to be present in your
    system.

8.  Commit your changes and push your branch to GitHub::

    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

9.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated. Put your
    new functionality into a function with a docstring, and add the feature to
    the list in README.md.

## Tips

### To run a subset of tests:

```sh
$ pytest tests/test_utils.py
```

### To run tox for a specific Python version

```sh
$ tox -e py27
```

[apiary ops]: http://docs.opsv31.apiary.io
[ops registration]: https://developers.epo.org/user/register
