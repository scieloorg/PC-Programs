import unittest
from unittest.mock import patch, Mock, ANY

import tempfile
import os
import shutil


from app_modules.generics.exporter import Exporter


class TestExporter(unittest.TestCase):

    def setUp(self):
        self.files_path = tempfile.mkdtemp()
        for item in "abc":
            with open(os.path.join(self.files_path, item), "w") as fp:
                fp.write(item)

    @patch('app_modules.generics.exporter.AsyncFTP')
    def test_export(self, MockAsyncFTP):
        data = dict(
            (
                ("server", "server"),
                ("password", "password"),
                ("remote_path", "remote_path"),
                ("user", "user"),
            )
        )

        exporter = Exporter(data)
        exporter.export(self.files_path, "xxx.zip")

        MockAsyncFTP.assert_called_once_with(
            ANY, "server", "user", "password", "remote_path"
        )

    @patch('app_modules.generics.exporter.logger')
    def test_export_raises_configuration_error(self, mk_logger):
        data = dict(
            (
                ("server", "server"),
                ("password", "password"),
                ("remote_path", "remote_path"),
            )
        )
        exporter = Exporter(data)
        exporter.ftp_configuration
        mk_logger.error.assert_called_once_with("Exporter: Missing FTP Configuration")

    def tearDown(self):
        shutil.rmtree(self.files_path)
