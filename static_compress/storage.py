from django.contrib.staticfiles.storage import StaticFilesStorage, ManifestStaticFilesStorage, CachedStaticFilesStorage

from . import mixin

__all__ = ["CompressedStaticFilesStorage", "CompressedManifestStaticFilesStorage", "CompressedCachedStaticFilesStorage"]


class CompressedStaticFilesStorage(mixin.CompressMixin, StaticFilesStorage):
    pass


class CompressedManifestStaticFilesStorage(mixin.CompressMixin, ManifestStaticFilesStorage):
    pass


class CompressedCachedStaticFilesStorage(mixin.CompressMixin, CachedStaticFilesStorage):
    pass
