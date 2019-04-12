import os
import tempfile
from pathlib import Path
import gzip

from django.test import SimpleTestCase
from django.core.management import call_command


class CollectStaticTest(SimpleTestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix='dsc_')
        self.temp_dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def assertFileExist(self, path):
        self.assertTrue(Path(path).exists(), "File {} should exists".format(path))

    def assertFileNotExist(self, path):
        self.assertFalse(Path(path).exists(), "File {} shouldn't exists".format(path))

    def assertStaticFiles(self):
        for file in ["milligram.css", "system.js", "speaker.svg"]:
            self.assertFileExist(self.temp_dir_path / file)
            self.assertFileExist(self.temp_dir_path / (file + ".gz"))
            self.assertFileExist(self.temp_dir_path / (file + ".br"))

        self.assertFileExist(self.temp_dir_path / "not_compressed.txt")

        for file in ["not_compressed.txt.gz", "not_compressed.txt.br"]:
            self.assertFileNotExist(self.temp_dir_path / file)

        for file in ("too_small.js.gz", "too_small.js.br"):
            self.assertFileNotExist(self.temp_dir_path / file)

    def assertManifestStaticFiles(self):
        for file in ["milligram.965a961f3962.css", "system.0177d7f30ce9.js", "speaker.5a6001289b0f.svg"]:
            self.assertFileExist(self.temp_dir_path / file)
            self.assertFileExist(self.temp_dir_path / (file + ".gz"))
            self.assertFileExist(self.temp_dir_path / (file + ".br"))

        self.assertFileExist(self.temp_dir_path / "not_compressed.9517ee88fcaa.txt")

        for file in ["not_compressed.9517ee88fcaa.txt.gz", "not_compressed.9517ee88fcaa.txt.br"]:
            self.assertFileNotExist(self.temp_dir_path / file)

        for file in ("too_small.1fad53895b9b.js.gz", "too_small.1fad53895b9b.js.br"):
            self.assertFileNotExist(self.temp_dir_path / file)

    def test_collectstatic_static(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)

            self.assertStaticFiles()

    def test_collectstatic_manifest(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedManifestStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)

            for file in ["milligram.css", "system.js", "not_compressed.txt", "speaker.svg", "staticfiles.json"]:
                self.assertFileExist(self.temp_dir_path / file)
                self.assertFileNotExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileNotExist(self.temp_dir_path / (file + ".br"))

            self.assertManifestStaticFiles()

    def test_collectstatic_cache(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedCachedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)

            for file in ["milligram.css", "system.js", "speaker.svg", "not_compressed.txt"]:
                self.assertFileExist(self.temp_dir_path / file)
                self.assertFileNotExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileNotExist(self.temp_dir_path / (file + ".br"))

            self.assertFileNotExist(self.temp_dir_path / "staticfiles.json")

            self.assertManifestStaticFiles()

    def test_collectstatic_only_gz(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_COMPRESS_METHODS=["gz"],
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)
            for file in ["milligram.css", "system.js", "speaker.svg"]:
                self.assertFileExist(self.temp_dir_path / file)
                self.assertFileExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileNotExist(self.temp_dir_path / (file + ".br"))

            self.assertFileExist(self.temp_dir_path / "not_compressed.txt")
            self.assertFileNotExist(self.temp_dir_path / "not_compressed.txt.gz")

    def test_collectstatic_changed_file_ext(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_COMPRESS_FILE_EXTS=("js", "css"),
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)
            for file in ("milligram.css", "system.js"):
                self.assertFileExist(self.temp_dir_path / file)
                self.assertFileExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileExist(self.temp_dir_path / (file + ".br"))

            self.assertFileExist(self.temp_dir_path / "speaker.svg")
            self.assertFileNotExist(self.temp_dir_path / "speaker.svg.gz")

    def test_collectstatic_empty_file_ext(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_COMPRESS_FILE_EXTS=[],
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)
            for file in ("milligram.css", "system.js", "speaker.svg"):
                self.assertFileExist(self.temp_dir_path / file)
                self.assertFileNotExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileNotExist(self.temp_dir_path / (file + ".br"))

    def test_collectstatic_not_keep_original(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_COMPRESS_KEEP_ORIGINAL=False,
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)
            for file in ("milligram.css", "system.js", "speaker.svg"):
                self.assertFileNotExist(self.temp_dir_path / file)
                self.assertFileExist(self.temp_dir_path / (file + ".gz"))
                self.assertFileExist(self.temp_dir_path / (file + ".br"))

    def test_collectstatic_with_zlib(self):
        with self.settings(
            STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
            STATIC_COMPRESS_MIN_SIZE_KB=1,
            STATIC_COMPRESS_METHODS=["gz+zlib", "br"],
            STATIC_ROOT=self.temp_dir.name,
        ):
            call_command("collectstatic", interactive=False, verbosity=0)

            self.assertStaticFiles()

    def test_collectstatic_twice_replace(self):
        with tempfile.TemporaryDirectory() as static_dir:
            with self.settings(
                STATICFILES_STORAGE="static_compress.storage.CompressedStaticFilesStorage",
                STATIC_COMPRESS_MIN_SIZE_KB=1,
                STATIC_COMPRESS_METHODS=["gz+zlib"],
                STATIC_ROOT=self.temp_dir.name,
                STATICFILES_DIRS=[static_dir],
            ):
                output_file_path = self.temp_dir_path / "test.js"
                compressed_file_path = self.temp_dir_path / "test.js.gz"

                static_file = Path(static_dir) / "test.js"
                with static_file.open("wb") as fp:
                    fp.write(b"a" * 5000)

                call_command("collectstatic", interactive=False, verbosity=0)

                self.assertFileExist(output_file_path)
                self.assertFileExist(compressed_file_path)

                # Fake that the file has been written long ago
                os.utime(output_file_path, times=(1, 1))
                os.utime(compressed_file_path, times=(1, 1))

                expected_content = b"b" * 5000
                with static_file.open("wb") as fp:
                    fp.write(expected_content)

                call_command("collectstatic", interactive=False, verbosity=0)

                self.assertEqual(output_file_path.read_bytes(), expected_content)

                with compressed_file_path.open("rb") as fp:
                    self.assertEqual(gzip.open(fp).read(), expected_content)
