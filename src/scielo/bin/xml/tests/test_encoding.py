# coding=utf-8

from unittest import TestCase, skipIf

import sys
from prodtools.utils import encoding


python_version = sys.version_info.major


@skipIf(python_version >= 3, "only apply for python < 3")
class TestEncodingPython2(TestCase):

    def test_decode_converts_input_type(self):
        self.assertEqual(encoding.decode("a"), u"a")

    def test_decode_keeps_input_value(self):
        self.assertEqual(encoding.decode(u"a"), u"a")

    def test_encode_converts_input_value(self):
        self.assertEqual(encoding.encode(u"a"), "a")

    def test_encode_keeps_input_value(self):
        self.assertEqual(encoding.encode("a"), "a")

    def test_encode_iso_converts_character_into_entities(self):
        self.assertEqual(encoding.encode(u"磨", "iso-8859-1"), "&#30952;")

    def test_encode_iso_does_not_convert_character_into_entities(self):
        self.assertEqual(encoding.encode(u"á", "iso-8859-1"), "\xe1")


@skipIf(python_version < 3, "only apply for python >= 3")
class TestEncoding(TestCase):

    def test_decode_converts_input_type(self):
        self.assertEqual(encoding.decode(b"a"), "a")

    def test_decode_keeps_input_value(self):
        self.assertEqual(encoding.decode("a"), "a")

    def test_encode_converts_input_value(self):
        self.assertEqual(encoding.encode("a"), b"a")

    def test_encode_keeps_input_value(self):
        self.assertEqual(encoding.encode(b"a"), b"a")

    def test_encode_iso_converts_character_into_entities(self):
        self.assertEqual(encoding.encode("磨", "iso-8859-1"), b"&#30952;")

    def test_encode_iso_does_not_convert_character_into_entities(self):
        self.assertEqual(encoding.encode("á", "iso-8859-1"), b"\xe1")
