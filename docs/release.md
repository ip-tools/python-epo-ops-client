# Release

Building Python packages and publishing to PyPI is automated
using the GHA workflow `release-pypi.yml`.

To release the package, exercise those steps:

- Edit `CHANGELOG.md`, designating a new version. Commit the file
  using a commit message like `Release 4.1.1`.

- Create a tag using the new version, including a `v` prefix, e.g.
  ```shell
  git tag v4.1.1
  ```

- Push to remote.
  ```shell
  git push && git push --tags
  ```
