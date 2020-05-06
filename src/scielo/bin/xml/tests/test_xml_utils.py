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
