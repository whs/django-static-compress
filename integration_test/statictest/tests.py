import tempfile
from pathlib import Path

from django.test import SimpleTestCase
from django.core.management import call_command


class CollectStaticTest(SimpleTestCase):
	def setUp(self):
		self.temp_dir = tempfile.TemporaryDirectory()
		self.temp_dir_path = Path(self.temp_dir.name)

	def tearDown(self):
		self.temp_dir.cleanup()

	def assertFileExist(self, path):
		self.assertTrue(Path(path).exists(), 'File {} should exists'.format(path))

	def assertFileNotExist(self, path):
		self.assertFalse(Path(path).exists(), 'File {} shouldn\'t exists'.format(path))

	def assertStaticFiles(self):
		for file in ['style.css', 'javascript.js', 'image.svg']:
			self.assertFileExist(self.temp_dir_path / file)
			self.assertFileExist(self.temp_dir_path / (file + '.gz'))
			self.assertFileExist(self.temp_dir_path / (file + '.br'))

		self.assertFileExist(self.temp_dir_path / 'not_compressed.txt')

		for file in ['not_compressed.txt.gz', 'not_compressed.txt.br']:
			self.assertFileNotExist(self.temp_dir_path / file)

	def assertManifestStaticFiles(self):
		for file in ['style.77e73540c2b9.css', 'javascript.1fad53895b9b.js', 'image.2c37c2ba6d07.svg']:
			self.assertFileExist(self.temp_dir_path / file)
			self.assertFileExist(self.temp_dir_path / (file + '.gz'))
			self.assertFileExist(self.temp_dir_path / (file + '.br'))

		self.assertFileExist(self.temp_dir_path / 'not_compressed.48dfde595e23.txt')

		for file in ['not_compressed.48dfde595e23.txt.gz', 'not_compressed.48dfde595e23.txt.br']:
			self.assertFileNotExist(self.temp_dir_path / file)

	def test_collectstatic_static(self):
		with self.settings(
			STATICFILES_STORAGE='static_compress.storage.CompressedStaticFilesStorage', STATIC_ROOT=self.temp_dir.name
		):
			call_command('collectstatic', interactive=False, verbosity=0)

			self.assertStaticFiles()

	def test_collectstatic_manifest(self):
		with self.settings(
			STATICFILES_STORAGE='static_compress.storage.CompressedManifestStaticFilesStorage', STATIC_ROOT=self.temp_dir.name
		):
			call_command('collectstatic', interactive=False, verbosity=0)

			for file in ['style.css', 'javascript.js', 'not_compressed.txt', 'image.svg', 'staticfiles.json']:
				self.assertFileExist(self.temp_dir_path / file)
				self.assertFileNotExist(self.temp_dir_path / (file + '.gz'))
				self.assertFileNotExist(self.temp_dir_path / (file + '.br'))

			self.assertManifestStaticFiles()

	def test_collectstatic_cache(self):
		with self.settings(
			STATICFILES_STORAGE='static_compress.storage.CompressedCachedStaticFilesStorage', STATIC_ROOT=self.temp_dir.name
		):
			call_command('collectstatic', interactive=False, verbosity=0)

			for file in ['style.css', 'javascript.js', 'image.svg', 'not_compressed.txt']:
				self.assertFileExist(self.temp_dir_path / file)
				self.assertFileNotExist(self.temp_dir_path / (file + '.gz'))
				self.assertFileNotExist(self.temp_dir_path / (file + '.br'))

			self.assertFileNotExist(self.temp_dir_path / 'staticfiles.json')

			self.assertManifestStaticFiles()
