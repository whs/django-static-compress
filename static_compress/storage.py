from django.contrib.staticfiles.storage import StaticFilesStorage, ManifestStaticFilesStorage

from . import mixin

__all__ = ["CompressedStaticFilesStorage", "CompressedManifestStaticFilesStorage"]


class CompressedStaticFilesStorage(mixin.CompressMixin, StaticFilesStorage):
    pass


class CompressedManifestStaticFilesStorage(mixin.CompressMixin, ManifestStaticFilesStorage):
    pass
