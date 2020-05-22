# coding=utf-8
import os
import sys
from unittest import TestCase


from prodtools.utils import xml_utils


python_version = sys.version_info.major


class TextEntity2Char(TestCase):
    def test_convert_converts_decimal_entity(self):
        text = "&#30952;"
        expected = "磨"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_named_entity(self):
        text = "&ccedil;&yuml;"
        expected = "çÿ"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_hexadecimal_entity(self):
        text = "&#x987;"
        expected = "ই"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_incomplete_entity(self):
        text = "&#30952&#x987"
        expected = "磨ই"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_incomplete_ccedil_entity(self):
        text = "&ccedil"
        expected = "ç"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_incomplete_ge_entity(self):
        text = "&ge."
        expected = "≥."
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_amp_plus_entity(self):
        text = "&amp;ccedil;&amp;#x987;"
        expected = "çই"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_amp_plus_incomplete_entity(self):
        text = "&amp;ccedil&amp;#x987"
        expected = "çই"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_does_not_convert_amp_entity(self):
        text = "&amp;"
        expected = "&amp;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_ge_entity(self):
        text = "&ge;"
        expected = "≥"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_does_not_convert_lt_and_gt_entity(self):
        text = "&lt;&gt;"
        expected = "&lt;&gt;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))


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

    def test_load_xml_return_errors_because_of_incomplete_tag(self):
        xml, errors = xml_utils.load_xml("<root")
        self.assertEqual(
            errors,
            "Loading XML from 'str': Couldn't find end of Start Tag root "
            "line 1, line 1, column 6 (<string>, line 1)")

    def test_load_return_errors_because_of_tag_which_does_not_close(
            self):
        xml, errors = xml_utils.load_xml("<root>")
        self.assertEqual(
            errors,
            "Loading XML from 'str': EndTag: '</' not found, "
            "line 1, column 7 (<string>, line 1)")

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

    def test_load_xml_loads_xml_but_ignore_incomplete_entities(self):
        xml, errors = xml_utils.load_xml("<root><a>&#91</a></root>")
        self.assertEqual(
            errors,
            "Loading XML from 'str': CharRef: invalid decimal value, "
            "line 1, column 14 (<string>, line 1)")


class TestRemoveStylesTags(TestCase):

    def test_remove_styles_off_tagged_content_removes_italic(self):
        text = "<root><source><italic>texto</italic></source></root>"
        expected = "<source>texto</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_off_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_off_tagged_content_removes_bold(self):
        text = "<root><source><bold>texto</bold></source></root>"
        expected = "<source>texto</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_off_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_off_tagged_content_does_not_remove_bold(self):
        text = "<root><source>texto 1 <bold>texto bold</bold> texto 2</source></root>"
        expected = "<source>texto 1 <bold>texto bold</bold> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_off_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_off_tagged_content_does_not_remove_italic(self):
        text = "<root><source>texto 1 <italic>texto italic</italic> texto 2</source></root>"
        expected = "<source>texto 1 <italic>texto italic</italic> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_off_tagged_content(node, ('bold', 'italic'))
        result = xml_utils.tostring(node)
        self.assertEqual(result, expected)

    def test_remove_styles_off_tagged_content_removes_external_and_keeps_inner(self):
        text = "<root><source><bold>texto 1 <bold>texto bold</bold> texto 2</bold></source></root>"
        expected = "<source>texto 1 <bold>texto bold</bold> texto 2</source>"
        obj = xml_utils.etree.fromstring(text)
        node = obj.find(".//source")
        xml_utils.remove_styles_off_tagged_content(node, ('bold', 'italic'))
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


class TestXMLRemoveFunctions(TestCase):

    def test_remove_attribute(self):
        text = """<root>
        <contrib contrib-type="editor">
            <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
            <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
            <name>
                <surname>Einstein</surname>
                <given-names>Albert</given-names>
            </name>
        </contrib>
        <contrib contrib-type="author">
            <contrib-id contrib-id-type="lattes">4760273612238540</contrib-id>
            <name>
                <surname>Meneghini</surname>
                <given-names>Rogerio</given-names>
            </name>
        </contrib></root>
        """
        root = xml_utils.etree.fromstring(text)
        xml_utils.remove_attribute(
            root, ".//contrib[@contrib-type='author']", "contrib-type")
        self.assertEqual(
            ['editor', None],
            [contrib.get("contrib-type")
             for contrib in root.findall(".//contrib")]
        )


class TestSuitableXML(TestCase):

    def test_init_xml_with_junk_is_loaded_without_errors(self):
        text = "<doc/> lixo"
        suitable_xml = xml_utils.SuitableXML(text)
        self.assertEqual(suitable_xml.format(), "<doc/>")
        self.assertIsNone(suitable_xml.xml_error)

    def test_init_xml_is_ok(self):
        text = "<doc/>"
        suitable_xml = xml_utils.SuitableXML(text)
        self.assertEqual(suitable_xml.format(), "<doc/>")
        self.assertIsNone(suitable_xml.xml_error)
        self.assertEqual(suitable_xml.doctype, '')
        self.assertIsNone(suitable_xml.xml_declaration)

    def test_init_xml_with_no_xml_declaration(self):
        text = ('<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
                'Publishing DTD v1.1 20151215//EN" '
                '"https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">'
                '\n<article/> lixo')
        suitable_xml = xml_utils.SuitableXML(text)
        self.assertIsNone(suitable_xml.xml_declaration)
        self.assertEqual(
            suitable_xml.doctype,
            '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
            'Publishing DTD v1.1 20151215//EN" "https://jats.nlm.nih.gov/'
            'publishing/1.1/JATS-journalpublishing1.dtd">')
        self.assertEqual(
            suitable_xml.format(),
            '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
            'Publishing DTD v1.1 20151215//EN" "https://jats.nlm.nih.gov/'
            'publishing/1.1/JATS-journalpublishing1.dtd">\n<article/>')

    def test_init_xml_with_no_doctype(self):
        text = '<?xml version="1.0" encoding="utf-8"?><doc/>'
        suitable_xml = xml_utils.SuitableXML(text)
        self.assertEqual(
            suitable_xml.xml_declaration,
            '<?xml version="1.0" encoding="utf-8"?>')
        self.assertEqual(suitable_xml.doctype, '')
        # self.assertEqual(
        #     '<?xml version="1.0" encoding="utf-8"?><doc/>',
        #     suitable_xml.format()
        # )

    def test_content_returns_characteres_instead_their_entities(self):
        text = ('<doc><p>&#91;&ccedil;&#93;</p> lixo</doc>')
        expected = ('<doc><p>[ç]</p> lixo</doc>')
        suitable_xml = xml_utils.SuitableXML(text)
        self.assertEqual(
            expected,
            suitable_xml.format())

    def test_well_formed_xml_content_removes_junk_after_last_close_tag(self):
        text = '<doc><p></p></doc> lixo'
        expected = '<doc><p/></doc>'
        suitable_xml = xml_utils.SuitableXML(text)
        suitable_xml.well_formed_xml_content()
        self.assertEqual(expected, suitable_xml.content)

    def test_well_formed_xml_content_removes_extra_spaces(self):
        text = """<doc><p><title>is nunc. Scelerisque in dictum non
        consectetur
        a erat nam. Ipsum dolor sit amet consectetur\t
        adipiscing elit duis tristique sollicitudin. \n
        Eu scelerisque felis imperdiet proin fermen</title></p></doc>"""
        expected = (
            '<doc><p><title>is nunc. Scelerisque in dictum non '
            'consectetur a erat nam. Ipsum dolor sit amet consectetur '
            'adipiscing elit duis tristique sollicitudin. Eu scelerisque '
            'felis imperdiet proin fermen</title></p></doc>')
        suitable_xml = xml_utils.SuitableXML(text)
        suitable_xml.well_formed_xml_content()
        self.assertEqual(expected, suitable_xml.content)

    def test_well_formed_xml_content_converts_entities_to_chars(self):
        text = '<doc><p>&#91;&ccedil;&#93;</p></doc>'
        expected = '<doc><p>[ç]</p></doc>'
        suitable_xml = xml_utils.SuitableXML(text)
        suitable_xml.well_formed_xml_content()
        self.assertEqual(expected, suitable_xml.content)

    def test_well_formed_xml_content_converts_quot_ent_to_chars(self):
        text = '<doc><p><a href=&quot;bla&quot;>teste</a></p></doc>'
        expected = '<doc><p><a href="bla">teste</a></p></doc>'
        suitable_xml = xml_utils.SuitableXML(text)
        suitable_xml.well_formed_xml_content()
        self.assertEqual(expected, suitable_xml.content)

