import unittest
from unittest.mock import patch, Mock, ANY

import tempfile
import os
import shutil


from prodtools.utils.exporter import Exporter


class TestExporter(unittest.TestCase):

    def setUp(self):
        self.files_path = tempfile.mkdtemp()
        for item in "abc":
            with open(os.path.join(self.files_path, item), "w") as fp:
                fp.write(item)

    @patch('prodtools.utils.exporter.FTP')
    def test_export(self, MockFTP):
        data = dict(
            (
                ("server", "server"),
                ("password", "password"),
                ("remote_path", "remote_path"),
                ("user", "user"),
            )
        )
        MockFTP.return_value = Mock(__enter__=MockFTP, __exit__=Mock())
        mock_ftp = MockFTP()

        exporter = Exporter(data)
        exporter.export(self.files_path, "xxx.zip")

        mock_ftp.login.assert_called_with("user", "password")
        mock_ftp.cwd.assert_called_with('remote_path')
        mock_ftp.storbinary.assert_called_with('STOR xxx.zip', ANY)

    def test_export_raises_configuration_error(self):
        data = dict(
            (
                ("server", "server"),
                ("password", "password"),
                ("remote_path", "remote_path"),
            )
        )
        exporter = Exporter(data)
        with self.assertRaises(KeyError) as exc_info:
            exporter.ftp_config
        self.assertEqual(
            str(exc_info.exception), "'Exporter: Configuration failure'")

    def tearDown(self):
        shutil.rmtree(self.files_path)
