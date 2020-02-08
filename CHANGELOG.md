# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Added a `Row` class to represent database query result rows. This is a subclass of `dict` that also includes lookup by index.

## [0.0.3] - 2019-01-19

### Fixed

- Correctly add charset to Content-Type header for text responses.
- Fix Content-Length header when body contains non-ASCII characters.

## [0.0.2] - 2019-01-14

### Added
- New `redirect` handler to redirect incoming requests to other locations.
- The `sql` template function now supports `file=` prefix, for loading SQL from a file.
- The `existsquery` column can now contain a `file=`-prefixed filename.
- The `json` handler can now use a `file=`-prefixed filename for its config.
- The `redirect` handler can now use a `file=`-prefixed filename for its config.

### Changed
- The SQLite database is now opened in read-only mode (`SQLITE_OPEN_READONLY`).
- BACKWARDS INCOMPATIBLE: changed to new `<type:param>` URL parameter syntax.
- BACKWARDS INCOMPATIBLE: changed the `exists_query` column to `existsquery`.


## [0.0.1] - 2019-01-12

Initial release.
