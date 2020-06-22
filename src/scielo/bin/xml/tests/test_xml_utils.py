# coding=utf-8
import os
import sys
import tempfile
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

    def test_convert_converts_amp_lt_entity(self):
        text = "&amp;lt;"
        expected = "&lt;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_converts_amp_gt_entity(self):
        text = "&amp;gt;"
        expected = "&gt;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_does_not_convert_lt_entity(self):
        text = "&lt;"
        expected = "&lt;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))

    def test_convert_does_not_convert_gt_entity(self):
        text = "&gt;"
        expected = "&gt;"
        obj = xml_utils.Entity2Char()
        self.assertEqual(expected, obj.convert(text))


class TestLoadXML(TestCase):

    def test_print_pretty_result_depends_on_the_param_remove_blank_text_of_load_xml(self):
        xml_input = (
            "<root><source><italic>texto 1</italic> <italic>texto 2</italic>"
            "</source></root>"
        )
        xml_with_blank_text_as_false, errors = xml_utils.load_xml(
            xml_input, remove_blank_text=False)
        result_with_blank_text_as_false = xml_utils.tostring(
            xml_with_blank_text_as_false, pretty_print=True)

        xml_with_blank_text_as_true, errors = xml_utils.load_xml(
            xml_input, remove_blank_text=True)
        result_with_blank_text_as_true = xml_utils.tostring(
            xml_with_blank_text_as_true, pretty_print=True)

        self.assertNotEqual(
            result_with_blank_text_as_false, result_with_blank_text_as_true)
        self.assertEqual(
            result_with_blank_text_as_false,
            "<root>\n"
            "  <source><italic>texto 1</italic> <italic>"
            "texto 2</italic></source>\n"
            "</root>\n"
        )
        self.assertEqual(
            result_with_blank_text_as_true,
            "<root>\n"
            "  <source>\n"
            "    <italic>texto 1</italic>\n"
            "    <italic>texto 2</italic>\n"
            "  </source>\n"
            "</root>\n"
        )

    def test_tostring_result_depends_on_the_param_remove_blank_text_of_load_xml(self):
        xml_input = (
            "<root><source><italic>texto 1</italic> <italic>texto 2</italic>"
            "</source></root>"
        )
        xml_with_blank_text_as_false, errors = xml_utils.load_xml(
            xml_input, remove_blank_text=False)
        result_with_blank_text_as_false = xml_utils.tostring(
            xml_with_blank_text_as_false)

        xml_with_blank_text_as_true, errors = xml_utils.load_xml(
            xml_input, remove_blank_text=True)
        result_with_blank_text_as_true = xml_utils.tostring(
            xml_with_blank_text_as_true)

        self.assertNotEqual(
            result_with_blank_text_as_false, result_with_blank_text_as_true)

        self.assertEqual(
            result_with_blank_text_as_false,
            "<root>"
            "<source><italic>texto 1</italic> <italic>"
            "texto 2</italic></source>"
            "</root>"
        )
        self.assertEqual(
            result_with_blank_text_as_true,
            "<root>"
            "<source><italic>texto 1</italic><italic>"
            "texto 2</italic></source>"
            "</root>"
        )

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

    def test_load_xml_with_remove_blank_text_as_true_remove_blanks(self):
        xml_input = (
            "<root><source><italic>texto 1</italic> <italic>texto 2</italic>"
            "</source></root>"
        )
        expected = (
            "<root><source><italic>texto 1</italic><italic>texto 2</italic>"
            "</source></root>"
        )
        xml, errors = xml_utils.load_xml(xml_input, remove_blank_text=True)
        result = xml_utils.tostring(xml)
        self.assertEqual(expected, result)

    def test_load_xml_with_remove_blank_text_as_false_keep_blanks(self):
        xml_input = (
            "<root><source><italic>texto 1</italic> <italic>texto 2</italic>"
            "</source></root>"
        )
        xml, errors = xml_utils.load_xml(
            "<root><source><italic>texto 1</italic> <italic>texto 2</italic>"
            "</source></root>",
            remove_blank_text=False)
        result = xml_utils.tostring(xml)
        self.assertEqual(xml_input, result)


class TestXMLinMultipleLines(TestCase):

    def test_insert_break_lines_uses_pretty_print(self):
        text = (
            "<root>"
            "<p>Texto 1 "
            "<bold>bold</bold> texto 2, "
            "<italic>texto italic</italic> "
            "<italic>outro italic</italic></p></root>"
            )
        expected = (
            "<root>"
            "\n  "
            "<p>Texto 1 "
            "<bold>bold</bold> texto 2, "
            "<italic>texto italic</italic> "
            "<italic>outro italic</italic></p>"
            "\n"
            "</root>"
            "\n"
            )
        content = xml_utils.insert_break_lines(text)
        self.assertEqual(expected, content)

    def test_insert_break_lines_uses_str_replace(self):
        text = (
            "<root>"
            "<p>Texto 1 "
            "<bold>bold</bold> texto 2, "
            "<italic>texto italic</italic> "
            "<italic>outro italic</italic></root>"
            )
        expected = (
            "<root>"
            "\n"
            "<p>Texto 1 "
            "\n"
            "<bold>bold</bold> texto 2, "
            "\n"
            "<italic>texto italic</italic> "
            "\n"
            "<italic>outro italic</italic></root>"
            )
        content = xml_utils.insert_break_lines(text)
        self.assertEqual(expected, content)

    def test_numbered_lines_prefixes_each_line_with_a_number(self):
        text = (
            "<root>\n"
            "<p>Texto 1 \n"
            "<bold>bold</bold> texto 2, \n"
            "<italic>texto italic</italic> \n"
            "<italic>outro italic</italic></root>"
            )
        expected = (
            "1: <root>\n"
            "2: <p>Texto 1 \n"
            "3: <bold>bold</bold> texto 2, \n"
            "4: <italic>texto italic</italic> \n"
            "5: <italic>outro italic</italic></root>"
            )
        content = xml_utils.numbered_lines(text)
        self.assertEqual(expected, content)


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

    def test_write_should_write_original_content_if_input_is_not_xml(self):
        text = "Qualquer texto nao XML."
        suitable_xml = xml_utils.SuitableXML(text)
        with tempfile.TemporaryDirectory() as xml_dir_path:
            xml_path = os.path.join(xml_dir_path, "xml_doc.xml")
            suitable_xml.write(xml_path)
            with open(xml_path) as xml_file:
                self.assertEqual(xml_file.read(), text)
        self.assertIsNotNone(suitable_xml.xml_error)
        self.assertIn("it must be an XML content or XML file path", suitable_xml.xml_error)

    def test_write_should_write_original_content_if_input_is_invalid_xml(self):
        text = ('<?xml version="1.0" encoding="utf-8"?>'
                '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
                'Publishing DTD v1.1 20151215//EN" '
                '"https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">'
                '\n<article>'
                '<p><ext-link ext-link-type="uri" xlink:href="<link-invalido>">bla</ext-link></p>'
                '</article>')
        suitable_xml = xml_utils.SuitableXML(text)
        with tempfile.TemporaryDirectory() as xml_dir_path:
            xml_path = os.path.join(xml_dir_path, "xml_doc.xml")
            suitable_xml.write(xml_path)

            with open(xml_path) as xml_file:
                self.assertEqual(xml_file.read(), text)
        self.assertIsNotNone(suitable_xml.xml_error)
        self.assertIn("Loading XML from 'str': ", suitable_xml.xml_error)

    def test_write_should_write_original_content_if_file_is_invalid_xml(self):
        text = ('<?xml version="1.0" encoding="utf-8"?>'
                '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
                'Publishing DTD v1.1 20151215//EN" '
                '"https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">'
                '<article>'
                '<p>Text</p>'
                '<back>'
                '</article>')

        with tempfile.TemporaryDirectory() as xml_dir_path:
            in_xml_path = os.path.join(xml_dir_path, "in_xml_doc.xml")
            with open(in_xml_path, 'w') as xml_file:
                xml_file.write(text)

            suitable_xml = xml_utils.SuitableXML(in_xml_path)
            out_xml_path = os.path.join(xml_dir_path, "out_xml_doc.xml")
            suitable_xml.write(out_xml_path)

            with open(out_xml_path) as xml_file:
                self.assertEqual(xml_file.read(), text)
        self.assertIsNotNone(suitable_xml.xml_error)
        self.assertIn("Loading XML from 'str': ", suitable_xml.xml_error)

    def test_write_should_write_corrected_xml_in_dest_file(self):
        text = ('<?xml version="1.0" encoding="utf-8"?>'
                '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
                'Publishing DTD v1.1 20151215//EN" '
                '"https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">'
                '<article><p>&amp;lt;</p></article>')
        
        with tempfile.TemporaryDirectory() as xml_dir_path:
            in_xml_path = os.path.join(xml_dir_path, "in_xml_doc.xml")
            with open(in_xml_path, 'w') as xml_file:
                xml_file.write(text)

            out_xml_path = os.path.join(xml_dir_path, "out_xml_doc.xml")
            suitable_xml = xml_utils.SuitableXML(in_xml_path)
            suitable_xml.write(out_xml_path)

            out_xml = xml_utils.etree.parse(out_xml_path)
            self.assertIsNotNone(out_xml.docinfo)
            self.assertEqual(out_xml.docinfo.xml_version, "1.0")
            self.assertEqual(out_xml.docinfo.encoding, "UTF-8")
            self.assertEqual(
                out_xml.docinfo.doctype,
                '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal '
                'Publishing DTD v1.1 20151215//EN" '
                '"https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">'
            )
            self.assertEqual(
                xml_utils.etree.tostring(out_xml.getroot()),
                b'<article>\n  <p>&lt;</p>\n</article>'
            )
            self.assertIsNone(suitable_xml.xml_error)

