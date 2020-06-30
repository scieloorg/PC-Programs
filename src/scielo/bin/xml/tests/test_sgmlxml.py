# coding=utf-8
import sys
from unittest import TestCase

from prodtools.processing import sgmlxml
from prodtools.utils import xml_utils


python_version = sys.version_info.major


class TestStyleTagsFixer(TestCase):

    def setUp(self):
        self.style_tags_fixer = sgmlxml.StyleTagsFixer()

    def test_restore_matched_style_tags_in_node_texts_returns_style_tags_in_upper_case(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</p></root>"""
        expected = """<root><p>texto 1 <SUP><BOLD>sup bold</BOLD></SUP> texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_texts(
                xml))

    def test_restore_matched_style_tags_in_node_texts_fixes_mismatched_tags(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        result = self.style_tags_fixer._restore_matched_style_tags_in_node_texts(
                xml)
        self.assertIn("<SUP>", result)
        self.assertIn("</SUP>", result)
        self.assertIn("<BOLD>", result)
        self.assertIn("</BOLD>", result)

    def test_fix_loading_xml_with_recover_true_fixes_mismatched_tags(self):
        text = """texto 1 [sup][bold]sup bold[/sup][/bold] texto 2"""
        xml = self.style_tags_fixer._fix_loading_xml_with_recover_true(
            text, None)
        result = xml_utils.tostring(xml)
        self.assertIn("<SUP>", result)
        self.assertIn("</SUP>", result)
        self.assertIn("<BOLD>", result)
        self.assertIn("</BOLD>", result)

    def test_restore_matched_style_tags_in_node_tails_returns_style_tags_in_upper_case(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</root>"""
        expected = """<root><p/>texto 1 <SUP><BOLD>sup bold</BOLD></SUP> texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_tails(
                xml))

    def test_restore_matched_style_tags_in_node_tails_fixes_mismatched_tags(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        result = self.style_tags_fixer._restore_matched_style_tags_in_node_tails(
                xml)
        self.assertIn("<SUP>", result)
        self.assertIn("</SUP>", result)
        self.assertIn("<BOLD>", result)
        self.assertIn("</BOLD>", result)

    def test_fix_inserting_tags_at_the_extremities_insert_at_the_start(self):
        text = """texto 1 [/sup] texto 2"""
        expected = """<SUP>texto 1 </SUP> texto 2"""
        result = self.style_tags_fixer._fix_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_fix_inserting_tags_at_the_extremities_insert_at_the_end(self):
        text = """texto 1 [sup] texto 2"""
        expected = """texto 1 <SUP> texto 2</SUP>"""
        result = self.style_tags_fixer._fix_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_fix_inserting_tags_at_the_extremities_insert_at_the_start_repeatly(self):
        text = """texto 1 [/sup][/bold][/italic][/sub] texto 2"""
        expected = """<SUB><ITALIC><BOLD><SUP>texto 1 </SUP></BOLD></ITALIC></SUB> texto 2"""
        result = self.style_tags_fixer._fix_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_fix_inserting_tags_at_the_extremities_insert_at_the_end_repeatly(self):
        text = """texto 1 [sub][italic][bold][sup] texto 2"""
        expected = """texto 1 <SUB><ITALIC><BOLD><SUP> texto 2</SUP></BOLD></ITALIC></SUB>"""
        result = self.style_tags_fixer._fix_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)
