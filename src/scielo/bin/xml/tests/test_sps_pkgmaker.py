# coding=utf-8
import sys
from unittest import TestCase

from app_modules.generics import xml_utils
from app_modules.app.pkg_processors import sps_pkgmaker


python_version = sys.version_info.major


class TestSPSXMLContent(TestCase):

    def test_remove_styles_from_tagged_content_removes_all_italics(self):
        text = "<root><source><italic>texto 1</italic> <italic>texto 2</italic></source></root>"
        expected = "<root><source>texto 1 texto 2</source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_from_tagged_content("source")
        self.assertEqual(obj.content, expected)

    def test_remove_styles_from_tagged_content_removes_bold_and_italics(self):
        text = "<root><source><bold> <italic>texto 1</italic> <italic>texto 2</italic> </bold></source></root>"
        expected = "<root><source> texto 1 texto 2 </source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_from_tagged_content("source")
        self.assertEqual(obj.content, expected)

    def test_remove_styles_from_tagged_content_does_not_remove_bold(self):
        text = "<root><source>texto 1 <bold>texto bold</bold> texto 2</source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_from_tagged_content("source")
        self.assertEqual(obj.content, text)

    def test_remove_styles_from_tagged_content_does_not_remove_italic(self):
        text = "<root><source><bold> <italic>texto 1</italic> sem estilo <italic>texto 2</italic> </bold></source></root>"
        expected = "<root><source> <italic>texto 1</italic> sem estilo <italic>texto 2</italic> </source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_from_tagged_content("source")
        self.assertEqual(obj.content, expected)


class TestBrokenRef(TestCase):

    def test_insert_label_text_in_mixed_citation_text_inserts_1(self):
        text = (
            '<ref id="B1">'
            '<label>1</label>'
            '<mixed-citation>. Aires M, Paz AA, Perosa CT. Situação de '
            'saúde e grau de dependência de pessoas idosas '
            'institucionalizadas. <italic>Rev Gaucha Enferm.</italic> '
            '2009;30(3):192-9.</mixed-citation>'
            '<element-citation/></ref>'
            )
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_label_text_in_mixed_citation_text()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").text,
            ("1. Aires M, Paz AA, Perosa CT. Situação de saúde e grau "
                "de dependência de pessoas idosas institucionalizadas. ")
        )
        self.assertEqual(obj.tree.find(".//label").text, "1")

    def test_insert_label_text_in_mixed_citation_text_removes_sep_off_mixed_citation_and_insert_1_and_dot(self):
        text = (
            '<ref id="B1">'
            '<label>1.</label>'
            '<mixed-citation>. Aires M, Paz AA, Perosa CT. Situação de '
            'saúde e grau de dependência de pessoas idosas '
            'institucionalizadas. <italic>Rev Gaucha Enferm.</italic> '
            '2009;30(3):192-9.</mixed-citation>'
            '<element-citation/></ref>'
            )
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_label_text_in_mixed_citation_text()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").text,
            ("1. Aires M, Paz AA, Perosa CT. Situação de saúde e grau "
                "de dependência de pessoas idosas institucionalizadas. ")
        )
        self.assertEqual(obj.tree.find(".//label").text, "1.")

    def test_insert_label_text_in_mixed_citation_text_do_nothing(self):
        text = (
            '<ref id="B1">'
            '<label>1.</label>'
            '<mixed-citation>1. Aires M, Paz AA, Perosa CT. Situação de '
            'saúde e grau de dependência de pessoas idosas '
            'institucionalizadas. <italic>Rev Gaucha Enferm.</italic> '
            '2009;30(3):192-9.</mixed-citation>'
            '<element-citation/></ref>'
            )
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_label_text_in_mixed_citation_text()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").text,
            ("1. Aires M, Paz AA, Perosa CT. Situação de saúde e grau "
                "de dependência de pessoas idosas institucionalizadas. ")
        )
        self.assertEqual(obj.tree.find(".//label").text, "1.")

    def test_insert_label_text_in_mixed_citation_text_inserts_1_and_dot(self):
        text = (
            '<ref id="B1">'
            '<label>1.</label>'
            '<mixed-citation>Aires M, Paz AA, Perosa CT. Situação de '
            'saúde e grau de dependência de pessoas idosas '
            'institucionalizadas. <italic>Rev Gaucha Enferm.</italic> '
            '2009;30(3):192-9.</mixed-citation>'
            '<element-citation/></ref>'
            )
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_label_text_in_mixed_citation_text()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").text,
            ("1. Aires M, Paz AA, Perosa CT. Situação de saúde e grau "
                "de dependência de pessoas idosas institucionalizadas. ")
        )
        self.assertEqual(obj.tree.find(".//label").text, "1.")

    def test_insert_label_text_in_mixed_citation_text_inserts_1_and_no_sep(self):
        text = (
            '<ref id="B1">'
            '<label>1</label>'
            '<mixed-citation>Aires M, Paz AA, Perosa CT. Situação de '
            'saúde e grau de dependência de pessoas idosas '
            'institucionalizadas. <italic>Rev Gaucha Enferm.</italic> '
            '2009;30(3):192-9.</mixed-citation>'
            '<element-citation/></ref>'
            )
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_label_text_in_mixed_citation_text()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").text,
            ("1 Aires M, Paz AA, Perosa CT. Situação de saúde e grau "
                "de dependência de pessoas idosas institucionalizadas. ")
        )
        self.assertEqual(obj.tree.find(".//label").text, "1")


class TestBrokenRefFixBookData(TestCase):
    def test_fix_book_data_does_not_convert_article_title_into_chapter_title(self):
        text = """<ref id="B02">
                <element-citation publication-type="book">
                    <article-title>Inflammatory bowel disease</article-title>
                    <chapter-title>...</chapter-title>
                </element-citation>
            </ref>"""
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.fix_book_data()
        self.assertEqual(
            "Inflammatory bowel disease",
            obj.tree.find(".//article-title").text
        )
        self.assertEqual(
            "...",
            obj.tree.find(".//chapter-title").text
        )

    def test_fix_book_data_converts_article_title_into_chapter_title(self):
        text = """<ref id="B02">
                <element-citation publication-type="book">
                    <article-title>Inflammatory bowel disease</article-title>
                    <source>...</source>
                </element-citation>
            </ref>"""
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.fix_book_data()
        self.assertEqual(
            "Inflammatory bowel disease",
            obj.tree.find(".//chapter-title").text
        )
        self.assertEqual(
            "...",
            obj.tree.find(".//source").text
        )

    def test_fix_book_data_converts_chapter_title_into_source_if_source_is_absent(self):
        text = """<ref id="B02">
                <element-citation publication-type="book">
                    <chapter-title>Inflammatory bowel disease</chapter-title>
                </element-citation>
            </ref>"""
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.fix_book_data()
        self.assertEqual(
            "Inflammatory bowel disease",
            obj.tree.find(".//source").text
        )
        self.assertIsNone(obj.tree.find(".//chapter-title"))

    def test_fix_book_data_converts_article_title_into_source_if_source_and_chapter_title_are_absent(self):
        text = """<ref id="B02">
                <element-citation publication-type="book">
                    <article-title>Inflammatory bowel disease</article-title>
                </element-citation>
            </ref>"""
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.fix_book_data()
        self.assertEqual(
            "Inflammatory bowel disease",
            obj.tree.find(".//source").text
        )
        self.assertIsNone(obj.tree.find(".//article-title"))
        self.assertIsNone(obj.tree.find(".//chapter-title"))

