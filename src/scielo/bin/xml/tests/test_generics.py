# coding=utf-8
import sys
import unittest
from app_modules.generics import fs_utils
from app_modules.generics import encoding
from app_modules.generics import xml_utils


header = """
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">
""".strip()

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


class TestXMLUtils(unittest.TestCase):

    def test_load_xml_loaded_from_file_content(self):
        text = fs_utils.read_file(
            "./tests/fixtures/0001-3765-aabc-92-s2-e20180981.xml")
        xml, error = xml_utils.load_xml(text)
        self.assertIsNone(error)

    def test_load_xml_loaded_from_file_path(self):
        xml, error = xml_utils.load_xml(
            "./tests/fixtures/0001-3765-aabc-92-s2-e20180981.xml")
        self.assertIsNone(error)

    def test_load_xml_returns_errors(self):
        text = fs_utils.read_file(
            "./tests/fixtures/0001-3765-aabc-92-s2-e20180981.xml")
        xml, error = xml_utils.load_xml(text[:400])
        self.assertIsNotNone(error)

    def test_tostring(self):
        if python_version < 3:
            text = u"""<root><article><title>Bá</title></article></root>"""
            expected = u"""<article><title>Bá</title></article>"""
        else:
            text = "<root><article><title>Bá</title></article></root>"
            expected = "<article><title>Bá</title></article>"
        xml, e = xml_utils.load_xml(header + text)
        node = xml.find(".//article")
        self.assertEqual(expected, xml_utils.tostring(node))

    def test_tostring_returns_type_equal_to_text(self):
        if python_version < 3:
            text = u"""<root><article><title>Bá</title></article></root>"""
            expected = u"""<article><title>Bá</title></article>"""
        else:
            text = "<root><article><title>Bá</title></article></root>"
            expected = "<article><title>Bá</title></article>"
        xml, e = xml_utils.load_xml(header + text)
        node = xml.find(".//article")
        self.assertEqual(type(expected), type(xml_utils.tostring(node, True)))

    @unittest.skip("")
    def test_tostring_returns_doctype(self):
        if python_version < 3:
            text = u"""<root><article><title>Bá</title></article></root>"""
            expected = u"""<article><title>Bá</title></article>"""
        else:
            text = "<root><article><title>Bá</title></article></root>"
            expected = "<article><title>Bá</title></article>"
        xml, e = xml_utils.load_xml(header + text)
        self.assertTrue(xml_utils.tostring(xml).startswith("<?xml"))

    def test_pretty_print_returns_pretty_print(self):
        if python_version < 3:
            text = u"""<root><article><title>Bá</title></article></root>"""
        else:
            text = "<root><article><title>Bá</title></article></root>"
        result = xml_utils.pretty_print(header + text)
        self.assertNotIn("<root><article>", result)
        self.assertIn("<root>", result)
        self.assertIn("<article>", result)
