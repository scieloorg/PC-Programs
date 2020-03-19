# coding=utf-8

from unittest import TestCase

import sys
from app_modules.generics import encoding


python_version = sys.version_info.major


class TestEncoding(TestCase):

    def setUp(self):
        print("Using Python {}".format(python_version))

    def test_decode_converts_input_type(self):
        if python_version < 3:
            return self.assertEqual(encoding.decode("a"), u"a")
        self.assertEqual(encoding.decode(b"a"), "a")

    def test_decode_keeps_input_value(self):
        if python_version < 3:
            return self.assertEqual(encoding.decode(u"a"), u"a")
        self.assertEqual(encoding.decode("a"), "a")

    def test_encode_converts_input_value(self):
        if python_version < 3:
            return self.assertEqual(encoding.encode(u"a"), "a")
        self.assertEqual(encoding.encode("a"), b"a")

    def test_encode_keeps_input_value(self):
        if python_version < 3:
            return self.assertEqual(encoding.encode("a"), "a")
        self.assertEqual(encoding.encode(b"a"), b"a")

    def test_encode_iso_converts_character_into_entities(self):
        if python_version < 3:
            return self.assertEqual(
                encoding.encode(u"磨", "iso-8859-1"), "&#30952;")
        self.assertEqual(encoding.encode("磨", "iso-8859-1"), b"&#30952;")

    def test_encode_iso_does_not_convert_character_into_entities(self):
        if python_version < 3:
            return self.assertEqual(
                encoding.encode(u"á", "iso-8859-1"), "\xe1")
        self.assertEqual(encoding.encode("á", "iso-8859-1"), b"\xe1")
