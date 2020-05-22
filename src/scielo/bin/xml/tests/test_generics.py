# coding=utf-8
import sys
import unittest


from prodtools.utils import fs_utils


python_version = sys.version_info.major


class TestFSUtils(unittest.TestCase):

    def test_read_file(self):
        text = fs_utils.read_file(
            "./tests/fixtures/arquivo-utf8.txt")
        if python_version < 3:
            self.assertIn(u"宿", text)
        else:
            self.assertIn("宿", text)

    def test_write_file(self):
        read_text = fs_utils.read_file(
            "./tests/fixtures/arquivo-utf8.txt")
        fs_utils.write_file(
            "./tests/fixtures/arquivo-utf8-written.txt", read_text)
        written_text = fs_utils.read_file(
            "./tests/fixtures/arquivo-utf8-written.txt")
        self.assertIn(written_text, read_text)

    def test_read_file_returns_none(self):
        self.assertIsNone(fs_utils.read_file("file_does_not_exist"))
