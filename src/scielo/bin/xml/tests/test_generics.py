# coding=utf-8
import sys
import unittest
from app_modules.generics import fs_utils
from app_modules.generics import encoding


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


class TestEncoding(unittest.TestCase):

    def test_encode(self):
        if python_version < 3:
            text = encoding.encode(u"blá")
            self.assertEqual(type(text), str)
        else:
            text = encoding.encode("blá")
            self.assertEqual(type(text), bytes)
