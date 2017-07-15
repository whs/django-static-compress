from django.core.files.base import ContentFile
import brotli
from zopfli import gzip as zopfli

__all__ = ['BrotliCompressor', 'ZopfliCompressor']

class BrotliCompressor:
	extension = 'br'

	def compress(self, path, file):
		return ContentFile(brotli.compress(file.read()))

class ZopfliCompressor:
	extension = 'gz'

	def compress(self, path, file):
		return ContentFile(zopfli.compress(file.read()))
