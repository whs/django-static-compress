# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2025-02-21
## Fixed
- Remove compressed files if one exists, but the original files is under `STATIC_COMPRESS_MIN_SIZE_KB`. (#211, thanks @Stegopoelkus)

## [2.0.0] - 2021-05-20
### Removed
- Remove `CompressedCachedStaticFilesStorage` as Django has removed it

## [1.2.1] - 2018-08-02

## Fixed

- Updated static's compressed file are now properly updated (#7, #8, thanks @hongquan)

## [1.2.0] - 2018-07-30

### Added

- Added the following settings (#2, thanks @hongquan)
  - `STATIC_COMPRESS_FILE_EXTS`
  - `STATIC_COMPRESS_METHODS`
  - `STATIC_COMPRESS_KEEP_ORIGINAL`
- Added method `gz+zlib` for gzip compression without Zopfli

### Changed

- Files smaller than 30kB are no longer compressed. This is the value that Webpack base on to split chunks
  - Set `STATIC_COMPRESS_MIN_SIZE_KB=0` to restore original behavior
- Added coding standard checkers and formatters

## [1.1.1] - 2017-12-24

### Changed

- Updated Brotli and Zopfli

[unreleased]: https://github.com/whs/django-static-compress/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/whs/django-static-compress/compare/v1.2.1...v2.0.0
[1.2.1]: https://github.com/whs/django-static-compress/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/whs/django-static-compress/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/whs/django-static-compress/compare/v1.1.0...v1.1.1
