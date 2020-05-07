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


class TestRemoveStylesTags(TestCase):
        
    def test_remove_styles_from_tagged_content_removes_italic(self):
        text = "<root><source><italic>texto</italic></source></root>"
        expected = "<source>texto</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_from_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_from_tagged_content_removes_bold(self):
        text = "<root><source><bold>texto</bold></source></root>"
        expected = "<source>texto</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_from_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_from_tagged_content_does_not_remove_bold(self):
        text = "<root><source>texto 1 <bold>texto bold</bold> texto 2</source></root>"
        expected = "<source>texto 1 <bold>texto bold</bold> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_from_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_from_tagged_content_does_not_remove_italic(self):
        text = "<root><source>texto 1 <italic>texto italic</italic> texto 2</source></root>"
        expected = "<source>texto 1 <italic>texto italic</italic> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_from_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_from_tagged_content_removes_external_and_keeps_inner(self):
        text = "<root><source><bold>texto 1 <bold>texto bold</bold> texto 2</bold></source></root>"
        expected = "<source>texto 1 <bold>texto bold</bold> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_from_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)


class TestMergeStylesTags(TestCase):

    def test_merge_siblings_style_tags_content_merges_italic(self):
        text = "<root><source>texto 0 <italic>texto 1</italic> <italic>texto 2</italic> </source></root>"
        expected = "<source>texto 0 <italic>texto 1 texto 2</italic> </source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.merge_siblings_style_tags_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_merge_siblings_style_tags_content_merges_bold(self):
        text = "<root><source><bold>texto 1</bold> <bold>texto 2</bold> </source></root>"
        expected = "<source><bold>texto 1 texto 2</bold> </source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.merge_siblings_style_tags_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_merge_siblings_style_tags_content_does_not_merge_sup(self):
        text = "<root><source><sup>texto 1</sup> <sup>texto 2</sup> </source></root>"
        expected = "<source><sup>texto 1</sup> <sup>texto 2</sup> </source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.merge_siblings_style_tags_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_merge_siblings_style_tags_content_does_not_merge_italic_if_there_are_elements_in_the_middle(self):
        text = "<root><source><italic>texto 1</italic> <bold>texto</bold> <italic>texto 2</italic></source></root>"
        expected = "<source><italic>texto 1</italic> <bold>texto</bold> <italic>texto 2</italic></source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.merge_siblings_style_tags_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_merge_siblings_style_tags_content_does_not_merge_italic_if_there_are_texts_in_the_middle(self):
        text = "<root><source><italic>texto 1</italic> texto <italic>texto 2</italic></source></root>"
        expected = "<source><italic>texto 1</italic> texto <italic>texto 2</italic></source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.merge_siblings_style_tags_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)


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
            broken.content, "<!DOCTYPE doctype ...>\n<doc/>")

    def test_init_xml_with_no_doctype(self):
        text = "<?xml version...?>\n<doc/> lixo"
        broken = xml_utils.BrokenXML(text)
        self.assertEqual(
            broken.processing_instruction, "<?xml version...?>")
        self.assertIsNone(broken.doctype)
        self.assertEqual(
            broken.content, "<?xml version...?>\n<doc/>")
