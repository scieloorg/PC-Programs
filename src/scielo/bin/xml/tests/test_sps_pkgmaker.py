# coding=utf-8
import sys
from unittest import TestCase

from prodtools.utils import xml_utils
from prodtools.processing import sps_pkgmaker


python_version = sys.version_info.major


class TestSPSXMLContent(TestCase):

    def test_remove_styles_off_tagged_content_removes_all_italics(self):
        text = "<root><source><italic>texto 1</italic> <italic>texto 2</italic></source></root>"
        expected = "<root><source>texto 1 texto 2</source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_off_tagged_content("source")
        self.assertEqual(obj.content, expected)

    def test_remove_styles_off_tagged_content_removes_bold_and_italics(self):
        text = "<root><source><bold> <italic>texto 1</italic> <italic>texto 2</italic> </bold></source></root>"
        expected = "<root><source>texto 1 texto 2</source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_off_tagged_content("source")
        self.assertEqual(obj.content, expected)

    def test_remove_styles_off_tagged_content_does_not_remove_bold(self):
        text = "<root><source>texto 1 <bold>texto bold</bold> texto 2</source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_off_tagged_content("source")
        self.assertEqual(obj.content, text)

    def test_remove_styles_off_tagged_content_does_not_remove_italic(self):
        text = "<root><source><bold> <italic>texto 1</italic> sem estilo <italic>texto 2</italic> </bold></source></root>"
        expected = "<root><source><italic>texto 1</italic> sem estilo <italic>texto 2</italic> </source></root>"
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_styles_off_tagged_content("source")
        self.assertEqual(obj.content, expected)

    def test_remove_uri_off_contrib_id(self):
        text = """<contrib-group>
        <contrib contrib-type="author">
            <contrib-id contrib-id-type="orcid">https://orcid.org/0000-0001-8528-2091</contrib-id>
            <contrib-id contrib-id-type="scopus">https://www.scopus.com/authid/detail.uri?authorId=24771926600</contrib-id>
            <name>
                <surname>Einstein</surname>
                <given-names>Albert</given-names>
            </name>
        </contrib>
        <contrib contrib-type="author">
            <contrib-id contrib-id-type="lattes">https://lattes.cnpq.br/4760273612238540</contrib-id>
            <name>
                <surname>Meneghini</surname>
                <given-names>Rogerio</given-names>
            </name>
        </contrib></contrib-group>"""
        obj = sps_pkgmaker.SPSXMLContent(text)
        obj.remove_uri_off_contrib_id()
        self.assertEqual(
            ['0000-0001-8528-2091', '24771926600', '4760273612238540'],
            [contrib_id.text
             for contrib_id in obj.xml.findall(".//contrib-id")]
        )


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


class TestBrokenRefLinksInMixedCitation(TestCase):

    def test_insert_ext_link_elements_in_mixed_citation(self):
        text = """<ref id="B04" xmlns:xlink="{}">
            <label>4</label>
            <mixed-citation>COB - Comitê Olímpico Brasileiro. Desafio para o corpo. Disponível em: http://www.cob.org.br/esportes/esporte.asp?id=39. (Acesso em 10 abr 2010)</mixed-citation>
            <element-citation publication-type="webpage">
                <person-group person-group-type="author">
                    <collab>COB -Comitê Olímpico Brasileiro</collab>
                </person-group>
                <source>Desafio para o corpo</source>
                <comment>Disponível em: <ext-link ext-link-type="uri" xlink:href="http://www.cob.org.br/esportes/esporte.asp?id=39">http://www.cob.org.br/esportes/esporte.asp?id=39</ext-link></comment>
                <date-in-citation content-type="access-date">10 abr 2010</date-in-citation>
            </element-citation>
        </ref>""".format(xml_utils.namespaces['xlink'])
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.insert_ext_link_elements_in_mixed_citation()
        self.assertEqual(
            obj.tree.find(".//mixed-citation").find(".//ext-link").text,
            obj.tree.find(".//element-citation").find(".//ext-link").text
        )


class TestBrokenRefSource(TestCase):

    def test_fix_source(self):
        text = """<ref-list>
            <ref id="B03">
                <label>3</label>
                <mixed-citation>LÉVY, Pierre. As tecnologias da inteligência: o futuro do pensamento na era da informática. Edição especial. Rio de Janeiro: Editora 34. 2001. 208 p.</mixed-citation>
                <element-citation publication-type="book">
                <source>As tecnologias da inteligência:o futuro do pensamento na era da informática</source>
            </element-citation>
            </ref>
        </ref-list>"""
        xml = xml_utils.etree.fromstring(text)
        obj = sps_pkgmaker.BrokenRef(xml)
        obj.fix_source()
        self.assertEqual((
            "As tecnologias da inteligência: o "
            "futuro do pensamento na era da informática"),
            obj.tree.find(".//source").text)

