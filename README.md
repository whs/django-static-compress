# Django-static-compress

Precompress your static files automatically with [Brotli](https://github.com/google/brotli) and [Zopfli](https://github.com/obp/zopfli)

## Installation

Install this from pip:

```sh
$ pip install django-static-compress
```

(you may want to write this in your requirements.txt)

Then update your settings.py:

```py
STATICFILES_STORAGE = 'static_compress.CompressedStaticFilesStorage'
```

When you run `python manage.py collectstatic` it will have an additional post-processing pass to compress your static files.

Make sure that your web server is configured to serve precompressed static files:

- If using nginx:
  - Setup [ngx_http_gzip_static_module](https://nginx.org/en/docs/http/ngx_http_gzip_static_module.html) to serve Zopfli (.gz) precompressed files.
  - Out of tree module [ngx_brotli](https://github.com/google/ngx_brotli) is required to serve Brotli (.br) precompressed files.
- [Caddy](https://caddyserver.com) will serve .gz and .br without additional configuration.

Also, as Brotli is not supported by all browsers you should make sure that your reverse proxy/CDN honor the Vary header, and your web server set it to [`Vary: Accept-Encoding`](https://blog.stackpath.com/accept-encoding-vary-important).

## Available storages

- `static_compress.CompressedStaticFilesStorage`: Generate `.br` and `.gz` from your static files
- `static_compress.CompressedManifestStaticFilesStorage`: Like [`ManifestStaticFilesStorage`](https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#manifeststaticfilesstorage), but also generate compressed files for the hashed files
- `static_compress.CompressedCachedStaticFilesStorage`: Like [`CachedStaticFilesStorage`](https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#cachedstaticfilesstorage), but also generate compressed files for the hashed files

You can also add support to your own backend by applying `static_compress.CompressMixin` to your class.

By default it will only compress files ending with `.js` and `.css`. This is controlled by the `allowed_extensions` instance attribute.

## File size reduction

Here's some statistics from [TipMe](https://tipme.in.th)'s jQuery and React bundle. Both bundle have related plugins built in with webpack (eg. Bootstrap for jQuery bundle, and [classnames](https://github.com/JedWatson/classnames) for React bundle), and is already minified.

```
101K jquery.9aa33728c6b5.js
 33K jquery.9aa33728c6b5.js.gz (33%)
 31K jquery.9aa33728c6b5.js.br (31%)
174K react.5c4899aeda53.js
 51K react.5c4899aeda53.js.gz (29%)
 44K react.5c4899aeda53.js.br (25%)
```

(.gz is Zopfli compressed, and .br is Brotli compressed)

## License

Licensed under the [MIT License](LICENSE)
