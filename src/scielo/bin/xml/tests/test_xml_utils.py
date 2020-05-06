# coding=utf-8
import os
import sys
from unittest import TestCase


from app_modules.generics import xml_utils


python_version = sys.version_info.major


class TestLoadXML(TestCase):

    def test_load_xml_successfully_from_str(self):
        xml, e = xml_utils.load_xml("<root/>")
        self.assertIsNone(e)
        self.assertIsNotNone(xml)

    def test_load_xml_successfully_from_file(self):
        with open("file.xml", "w") as fp:
            fp.write("<root/>")
        xml, e = xml_utils.load_xml("file.xml")
        self.assertIsNone(e)
        self.assertIsNotNone(xml)
        os.unlink("file.xml")

    def test_load_xml_syntax_error_for_incomplete_tag(self):
        xml, errors = xml_utils.load_xml("<root")
        self.assertIsNone(xml)
        self.assertEqual(
            ("Loading XML from 'str': "
             "Couldn't find end of Start Tag root line 1, "
             "line 1, column 6 (<string>, line 1)"),
            errors
        )

    def test_load_xml_syntax_error_for_tag_which_does_not_close(self):
        xml, errors = xml_utils.load_xml("<root>")
        self.assertIsNone(xml)
        self.assertEqual(
            ("Loading XML from 'str': "
             "EndTag: '</' not found, "
             "line 1, column 7 (<string>, line 1)"),
            errors
        )

    def test_load_xml_from_not_a_file_and_not_xml(self):
        xml, errors = xml_utils.load_xml("notfile_notxml")
        self.assertIsNone(xml)
        self.assertEqual(
            ("Loading XML from 'notfile_notxml': "
             "Invalid value: it must be an XML content or XML file path"),
            errors
        )

    def test_load_xml_from_not_found_file(self):
        xml, errors = xml_utils.load_xml("notfoundfile.xml")
        self.assertIsNone(xml)
        self.assertEqual(
            ("Loading XML from 'notfoundfile.xml': "
             "Error reading file 'notfoundfile.xml': "
             "failed to load external entity \"notfoundfile.xml\""),
            errors
        )


class TestBrokenXML(TestCase):

    def test_init_xml_with_junk_is_loaded_without_errors(self):
        text = "<doc/> lixo"
        broken = xml_utils.BrokenXML(text)
        self.assertEqual(broken.content, "<doc/>")
        self.assertIsNone(broken.xml_error)

    def test_init_xml_is_ok(self):
        text = "<doc/>"
        broken = xml_utils.BrokenXML(text)
        self.assertEqual(broken.content, "<doc/>")
        self.assertIsNone(broken.xml_error)
        self.assertIsNone(broken.doctype)
        self.assertIsNone(broken.processing_instruction)

    def test_init_xml_with_no_processing_instruction(self):
        text = "<!DOCTYPE doctype ...>\n<doc/> lixo"
        broken = xml_utils.BrokenXML(text)
        self.assertIsNone(broken.processing_instruction)
        self.assertEqual(
            broken.doctype, "<!DOCTYPE doctype ...>")
        self.assertEqual(
            broken.content, "<doc/>")

    def test_init_xml_with_no_doctype(self):
        text = "<?xml version...?>\n<doc/> lixo"
        broken = xml_utils.BrokenXML(text)
        self.assertEqual(
            broken.processing_instruction, "<?xml version...?>")
        self.assertIsNone(broken.doctype)
        self.assertEqual(
            broken.content, "<doc/>")
