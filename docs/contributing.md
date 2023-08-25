# Contributing

Contributions are welcome, and they are greatly appreciated. Every bit
helps, and credit will always be given. You can contribute in many ways.

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/ip-tools/python-epo-ops-client/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to
whoever wants to fix it.

### Implement Features

We are tracking all sorts of tasks within the [backlog](backlog.md) file and
as issues on GitHub. Just pick one, submit a corresponding patch, or start
a discussion around it. Anything tagged with "feature" is open to whoever wants
to implement it.

### Write Documentation

python-epo-ops-client could always use more documentation, whether as part of
the official python-epo-ops-client docs, in docstrings, or even on the web in
blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/ip-tools/python-epo-ops-client/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are
  welcome. 😊

## Get Started!

Ready to contribute? Here's how to set up `python-epo-ops-client` for local
development. Before going into the forking process, you should first [install
a development sandbox](sandbox.md).

1.  Fork the `python-epo-ops-client` repository on GitHub and clone your fork.
    ```shell
    git clone git@github.com:[your_name_here]/python-epo-ops-client.git
    cd python-epo-ops-client/
    ```

4.  Create a branch for local development:
    ```shell
    git switch -c <branchname>
    ```
    Now, make your changes within your working tree.

5.  After making changes to the code base, you may want to check that your
    changes pass test and linting procedures. For that purpose, run
    `make check`.

6.  Commit your changes and push your branch to GitHub.

    ```shell
    git add .
    git commit -m "A detailed description of your changes."
    git push origin <branchname>
    ```

7.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated. Put your
    new functionality into a function with a docstring, and add the feature to
    the list in README.md.
