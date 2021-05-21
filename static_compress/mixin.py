import os
from collections import OrderedDict
from os.path import getatime, getctime, getmtime
import errno

from django.core.exceptions import ImproperlyConfigured

from . import compressors

__all__ = ["CompressMixin"]


DEFAULT_METHODS = ["gz", "br"]
METHOD_MAPPING = {
    "gz": compressors.ZopfliCompressor,
    "br": compressors.BrotliCompressor,
    "gz+zlib": compressors.ZlibCompressor,
    # gz+zlib and gz cannot be used at the same time, because they produce the same file extension.
}


class CompressMixin:
    allowed_extensions = []
    compress_methods = []
    keep_original = True
    compressors = []
    minimum_kb = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We access Django settings lately here, to allow our app to be imported without
        # defining DJANGO_SETTINGS_MODULE.
        from django.conf import settings

        self.allowed_extensions = getattr(settings, "STATIC_COMPRESS_FILE_EXTS", ["js", "css", "svg"])
        self.compress_methods = getattr(settings, "STATIC_COMPRESS_METHODS", DEFAULT_METHODS)
        self.keep_original = getattr(settings, "STATIC_COMPRESS_KEEP_ORIGINAL", True)
        self.minimum_kb = getattr(settings, "STATIC_COMPRESS_MIN_SIZE_KB", 0)

        valid = [i for i in self.compress_methods if i in METHOD_MAPPING]
        if not valid:
            raise ImproperlyConfigured("No valid method is defined in STATIC_COMPRESS_METHODS setting.")
        if "gz" in valid and "gz+zlib" in valid:
            raise ImproperlyConfigured("STATIC_COMPRESS_METHODS: gz and gz+zlib cannot be used at the same time.")
        self.compressors = [METHOD_MAPPING[k]() for k in valid]

    def get_alternate_compressed_path(self, name):
        for compressor in self.compressors:
            ext = compressor.extension
            if name.endswith(".{}".format(ext)):
                path = self.path(name)
            else:
                path = self.path("{}.{}".format(name, ext))
            if os.path.exists(path):
                return path
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    def get_accessed_time(self, name):
        if self.keep_original:
            return super().get_accessed_time(name)
        return self._datetime_from_timestamp(getatime(self.get_alternate_compressed_path(name)))

    def get_created_time(self, name):
        if self.keep_original:
            return super().get_created_time(name)
        return self._datetime_from_timestamp(getctime(self.get_alternate_compressed_path(name)))

    def get_modified_time(self, name):
        if self.keep_original:
            return super().get_modified_time(name)
        alt = self.get_alternate_compressed_path(name)
        return self._datetime_from_timestamp(getmtime(alt))

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        files = OrderedDict()

        super_class = super()
        if hasattr(super_class, "post_process"):
            generator = super_class.post_process(paths, dry_run, **options)
        else:
            generator = iter((f, f, False) for f in paths)

        for file, hashed_file, processed in generator:
            files[file] = hashed_file
            yield file, hashed_file, processed

        for name in paths.keys():
            if not (name in files and self._is_file_allowed(name)):
                continue

            source_storage, _ = paths[name]

            path = files[name]
            # Process if file is big enough
            real_path = self.path(path)
            if self.minimum_kb and os.path.getsize(real_path) < self.minimum_kb * 1024:
                continue

            with self._open(real_path) as file:
                for compressor in self.compressors:
                    dest_compressed_name = "{}.{}".format(path, compressor.extension)
                    dest_compressed_path = self.path(dest_compressed_name)

                    # Check if the original file has been changed.
                    # If not, no need to compress again.
                    try:
                        if hasattr(self, 'hashed_name'):  # compute on hash value. if file exists so is it up to date
                            file_is_unmodified = self.exists(dest_compressed_name)
                        else:
                            src_mtime = source_storage.get_modified_time(path)
                            dest_mtime = self._datetime_from_timestamp(getmtime(dest_compressed_path))
                            file_is_unmodified = dest_mtime.replace(microsecond=0) >= src_mtime.replace(microsecond=0)
                    except FileNotFoundError:
                        file_is_unmodified = False
                    if file_is_unmodified:
                        yield path, dest_compressed_name, False
                        continue

                    # Delete old gzip file, or Nginx will pick the old file to serve.
                    # Note: Django won't overwrite the file, so we have to delete it ourselves.
                    if self.exists(dest_compressed_path):
                        self.delete(dest_compressed_path)
                    out = compressor.compress(path, file)

                    if out:
                        self._save(dest_compressed_path, out)
                        if not self.keep_original:
                            self.delete(name)
                        yield path, dest_compressed_name, True

                    file.seek(0)

    def _get_dest_path(self, path):
        if hasattr(self, "hashed_name"):
            return self.hashed_name(path)

        return path

    def _is_file_allowed(self, file):
        for extension in self.allowed_extensions:
            if file.endswith("." + extension):
                return True
        return False
