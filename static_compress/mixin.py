from . import compressors

__all__ = ['CompressMixin']


class CompressMixin:
	allowed_extensions = ['js', 'css', 'svg']
	compressors = [compressors.BrotliCompressor(), compressors.ZopfliCompressor()]

	def post_process(self, paths, dry_run=False, **options):
		if hasattr(super(), 'post_process'):
			yield from super().post_process(paths, dry_run, **options)

		if dry_run:
			return

		for name in paths.keys():
			if not self._is_file_allowed(name):
				continue

			_, path = paths[name]
			dest_path = self._get_dest_path(path)
			with self._open(dest_path) as file:
				for compressor in self.compressors:
					dest_compressor_path = dest_path + '.' + compressor.extension
					out = compressor.compress(path, file)

					if out:
						self._save(dest_compressor_path, out)
						yield dest_path, dest_compressor_path, True

					file.seek(0)

	def _get_dest_path(self, path):
		if hasattr(self, 'hashed_name'):
			return self.hashed_name(path)

		return path

	def _is_file_allowed(self, file):
		for extension in self.allowed_extensions:
			if file.endswith('.' + extension):
				return True
		return False
