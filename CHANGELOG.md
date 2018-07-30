# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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


## [1.1.1] - 2017-12-24
### Changed
- Updated Brotli and Zopfli

[Unreleased]: https://github.com/whs/django-static-compress/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/whs/django-static-compress/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/whs/django-static-compress/compare/v1.1.0...v1.1.1
