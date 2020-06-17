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
            self.style_tags_fixer._restore_matched_style_tags_in_node_texts(
                xml))

    def test_restore_matched_style_tags_in_node_texts_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        expected = """<root><p>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</p></root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_texts(
                xml))

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

    def test_restore_matched_style_tags_in_node_tail_with_retry_true_restores_them_although_they_are_mismatched(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        self.style_tags_fixer._restore_matched_style_tags_in_node_tail(
            node, retry=True)
        self.assertEqual(node.tail, "texto 1 ")
        self.assertEqual(
            xml_utils.tostring(node.getnext()),
            "<sup><bold>sup bold</bold></sup>")
        self.assertEqual(node.getnext().tail, " texto 2")

    def test_restore_matched_style_tags_in_node_tail_with_retry_true_restores_sup_although_it_is_not_closed(self):
        text = """<root><p/>texto 1 [sup]sup bold texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        node = xml.find(".//p")
        self.style_tags_fixer._restore_matched_style_tags_in_node_tail(
            node, retry=True)
        self.assertEqual(node.tail, "texto 1 ")
        self.assertEqual(
            xml_utils.tostring(node.getnext()),
            "<sup>sup bold texto 2</sup>")
        self.assertEqual(node.getnext().tail, None or "")

    def test_restore_matched_style_tags_in_node_tails_returns_restored_style_tags(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/bold][/sup] texto 2</root>"""
        expected = """<root><p/>texto 1 <sup><bold>sup bold</bold></sup> texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_tails(
                xml))

    def test_restore_matched_style_tags_in_node_tails_does_not_restore_because_they_are_mismatched(self):
        text = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        expected = """<root><p/>texto 1 [sup][bold]sup bold[/sup][/bold] texto 2</root>"""
        xml = xml_utils.etree.fromstring(text)
        self.assertEqual(
            expected,
            self.style_tags_fixer._restore_matched_style_tags_in_node_tails(
                xml))

    def test_retry_inserting_tags_at_the_extremities_insert_at_the_start(self):
        text = """texto 1 </sup> texto 2"""
        expected = """<sup>texto 1 </sup> texto 2"""
        result = self.style_tags_fixer._retry_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_retry_inserting_tags_at_the_extremities_insert_at_the_end(self):
        text = """texto 1 <sup> texto 2"""
        expected = """texto 1 <sup> texto 2</sup>"""
        result = self.style_tags_fixer._retry_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_retry_inserting_tags_at_the_extremities_insert_at_the_start_repeatly(self):
        text = """texto 1 </sup></bold></italic></sub> texto 2"""
        expected = """<sub><italic><bold><sup>texto 1 </sup></bold></italic></sub> texto 2"""
        result = self.style_tags_fixer._retry_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)

    def test_retry_inserting_tags_at_the_extremities_insert_at_the_end_repeatly(self):
        text = """texto 1 <sub><italic><bold><sup> texto 2"""
        expected = """texto 1 <sub><italic><bold><sup> texto 2</sup></bold></italic></sub>"""
        result = self.style_tags_fixer._retry_inserting_tags_at_the_extremities(
            text)
        self.assertEqual(expected, result)
