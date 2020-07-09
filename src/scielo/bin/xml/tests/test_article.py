from unittest import TestCase

from prodtools.data.article import Article
from prodtools.utils import xml_utils


class TestArticle(TestCase):

    def test_is_bibr_xref_number_returns_true(self):
        text = (
            '<article>'
            '<body><p><xref ref-type="bibr" rid="B01">(1)</xref></p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.is_bibr_xref_number
        expected = True
        self.assertEqual(expected, result)

    def test_is_bibr_xref_number_returns_false(self):
        text = (
            '<article>'
            '<body><p><xref ref-type="bibr" rid="B01">(a1)</xref></p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.is_bibr_xref_number
        expected = False
        self.assertEqual(expected, result)

    def test_is_bibr_xref_number_returns_false_for_sup_a1(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>(a1)</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.is_bibr_xref_number
        expected = False
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_dict_bibr_as_key_and_empty_list_as_value(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>(a1)</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {"bibr": []}
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_dict_bibr_as_key_and_empty_list_as_value_because_it_is_not_a_range(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>(a1)</sup></xref>'
            '-<xref ref-type="bibr" rid="B01"><sup>(a1)</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {"bibr": []}
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_dict_bibr_as_key_and_one_item_list(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>1</sup></xref>'
            '-<xref ref-type="bibr" rid="B02"><sup>2</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {
            "bibr":
            [[1, 2, xml.find(".//xref[1]"), xml.find(".//xref[2]")]]}
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_dict_with_two_items(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>1</sup></xref>'
            '-<xref ref-type="bibr" rid="B02"><sup>2</sup></xref>'
            '<xref ref-type="bibr" rid="B05"><sup>5</sup></xref>'
            '-<xref ref-type="bibr" rid="B08"><sup>8</sup></xref>'
            '<xref ref-type="fig" rid="f01"><sup>1</sup></xref>'
            '-<xref ref-type="fig" rid="f02"><sup>2</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {
            "bibr":
                [[1, 2, xml.find(".//xref[1]"), xml.find(".//xref[2]")],
                 [5, 8, xml.find(".//xref[3]"), xml.find(".//xref[4]")],
                 ],
            "fig":
                [[1, 2, xml.find(".//xref[5]"), xml.find(".//xref[6]")]]
        }
        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_one_parent_and_one_xref(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {"bibr": []}

        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_one_parent_and_two_xref(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '-<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {
            "bibr":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[1]"),
                     xml.find(".//xref[2]")]),
                 ],
        }
        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_two_parents_and_six_children(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">1</xref>'
            '-<xref ref-type="bibr" rid="B02">2</xref>'
            '<xref ref-type="bibr" rid="B05">5</xref>'
            '-<xref ref-type="bibr" rid="B08">8</xref>'
            '<xref ref-type="fig" rid="f01">1</xref>'
            '-<xref ref-type="fig" rid="f02">2</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {
            "bibr":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[1]"),
                     xml.find(".//xref[2]"),
                     xml.find(".//xref[3]"),
                     xml.find(".//xref[4]"),
                     ]),
                 ],
            "fig":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[5]"),
                     xml.find(".//xref[6]")]),
                 ],
        }
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_dict_with_two_items(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01"><sup>1</sup></xref>'
            '-<xref ref-type="bibr" rid="B02"><sup>2</sup></xref>'
            '<xref ref-type="bibr" rid="B05"><sup>5</sup></xref>'
            '-<xref ref-type="bibr" rid="B08"><sup>8</sup></xref>'
            '<xref ref-type="fig" rid="f01"><sup>1</sup></xref>'
            '-<xref ref-type="fig" rid="f02"><sup>2</sup></xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {
            "bibr":
                [[1, 2, xml.find(".//xref[1]"), xml.find(".//xref[2]")],
                 [5, 8, xml.find(".//xref[3]"), xml.find(".//xref[4]")],
                 ],
            "fig":
                [[1, 2, xml.find(".//xref[5]"), xml.find(".//xref[6]")]]
        }
        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_one_parent_and_one_xref(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {"bibr": []}

        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_one_parent_and_two_xref(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '-<xref ref-type="bibr" rid="B01">(a1)</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {
            "bibr":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[1]"),
                     xml.find(".//xref[2]")]),
                 ],
        }
        self.assertEqual(expected, result)

    def test_any_xref_parent_nodes_returns_two_parents_and_six_children(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">1</xref>'
            '-<xref ref-type="bibr" rid="B02">2</xref>'
            '<xref ref-type="bibr" rid="B05">5</xref>'
            '-<xref ref-type="bibr" rid="B08">8</xref>'
            '<xref ref-type="fig" rid="f01">1</xref>'
            '-<xref ref-type="fig" rid="f02">2</xref>'
            '</p></body>'
            '</article>'
        )
        xml, error = xml_utils.load_xml(text)
        a = Article(xml, "nome")
        result = a.any_xref_parent_nodes
        expected = {
            "bibr":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[1]"),
                     xml.find(".//xref[2]"),
                     xml.find(".//xref[3]"),
                     xml.find(".//xref[4]"),
                     ]),
                 ],
            "fig":
                [(xml.find(".//p[1]"),
                    [xml.find(".//xref[5]"),
                     xml.find(".//xref[6]")]),
                 ],
        }
        self.assertEqual(expected, result)
