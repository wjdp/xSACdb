# Releasing xSACdb


## master branch - the 'next' tag

Every push on the master branch triggers a CI pipeline which, if it passes, will automatically release the docker tag `wjdp/xsacdb:next`.

The staging environment https://next.xsacdb.wjdp.uk watches for changes in this tag and will automatically deploy if a newer version is available.


## Tagged versions - vX.Y.Z

We loosely follow https://semver.org/ as we're an application rather than a library.

- **Major** version should be bumped to indicate a radical change in the usage of the application or to indicate a major milestone for the project.
- **Minor** version should be bumped when features are added or changed.
- **Patch** version should be bumped for bug fixes.

To release a version for production use follow these steps:

1. Pull the latest master locally.
2. Ensure the [CHANGELOG](CHANGELOG.md) has been kept up to date by cross-referencing with the git log.
3. Change the 'Unreleased' heading in the CHANGELOG to the version number to be released and today's date.
4. Add and commit just the CHANGELOG changes with the commit message `Release vX.Y.Z`.
5. Tag this commit like so `git tag -am "" vX.Y.Z`.
6. Push the master branch followed by the new tag.

A CI pipeline will be triggered for the commit, updating the `wjdp/xsacdb:next` image.

Another pipeline will build and release the `wjdp/xsacdb:vX.Y.Z` and `wjdp/xsacdb:latest` image.

The staging environment https://current.xsacdb.wjdp.uk watches for changes in the `latest` tag and will automatically deploy if a newer version is available.
This can be used for final checks before upgrading club instances.
