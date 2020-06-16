# coding=utf-8
import sys
from unittest import TestCase

from prodtools.processing import sgmlxml
from prodtools.utils import xml_utils


python_version = sys.version_info.major


class TestStyleTagsFixer(TestCase):

    def setUp(self):
        self.style_tags_fixer = sgmlxml.StyleTagsFixer()

    def test_restore_matched_style_tags_in_node_text_returns_restored_style_tags(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        new_node = self.style_tags_fixer._restore_matched_style_tags_in_node_text(node)
        expected = """<p>texto 1 <sup><bold>sup bold</bold></sup> texto 2</p>"""
        self.assertEqual(
            expected, xml_utils.tostring(new_node))

    def test_restore_matched_style_tags_in_node_text_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        new_node = self.style_tags_fixer._restore_matched_style_tags_in_node_text(node)
        self.assertIsNone(xml_utils.tostring(new_node))

    def test_restore_matched_style_tags_in_node_texts_returns_restored_style_tags(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</p></root>"""
        expected = """<root><p>texto 1 <sup><bold>sup bold</bold></sup> texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_texts(xml))

    def test_restore_matched_style_tags_in_node_texts_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        expected = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_texts(xml))

    def test_restore_matched_style_tags_in_node_tail_returns_restored_style_tags(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        self.style_tags_fixer._restore_matched_style_tags_in_node_tail(node)
        self.assertEqual(node.tail, "texto 1 ")
        self.assertEqual(
            xml_utils.tostring(node.getnext()),
            "<sup><bold>sup bold</bold></sup>")
        self.assertEqual(node.getnext().tail, " texto 2")

    def test_restore_matched_style_tags_in_node_tail_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        self.style_tags_fixer._restore_matched_style_tags_in_node_tail(node)
        self.assertEqual(
            node.tail, "texto 1 [sup][bold]sup bold[/sup][/bold] texto 2")

    def test_restore_matched_style_tags_in_node_tails_returns_restored_style_tags(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</root>"""
        expected = """<root><p/>texto 1 <sup><bold>sup bold</bold></sup> texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_tails(xml))

    def test_restore_matched_style_tags_in_node_tails_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        expected = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_tails(xml))
