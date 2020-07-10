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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
        a = Article(xml, "nome")
        result = a.any_xref_ranges
        expected = {
            "bibr":
            [[1, 1, xml.find(".//xref[1]"), xml.find(".//xref[2]")]]}
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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
        xml = xml_utils.etree.fromstring(text)
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


class TestArticleXref(TestCase):

    def setUp(self):
        text = """<article><body>
        <p>Los estudios históricos sobre ... 
        me refiero a las listas de A. 
        <xref ref-type="bibr" rid="B61">Thurm (1883</xref>) o de Th. 
        <xref ref-type="bibr" rid="B9">Botten-Wobst (1876</xref>); 
        además, este último se ocupa solo de las misiones en Roma. 
        Hay un trabajo más reciente, el de P. 
        <xref ref-type="bibr" rid="B43">Knibbe (1958</xref>), 
        ... por E. <xref ref-type="bibr" rid="B44">Krug (1916</xref>);
        y el segundo es el realizado por B.
        <xref ref-type="bibr" rid="B54">Schleussner (1978</xref>), 
        a los escritos de C. 
        <xref ref-type="bibr" rid="B48">Phillipson (1911</xref>), 
        de P. <xref ref-type="bibr" rid="B68">Willems (1878</xref>-1885), 
        de P. <xref ref-type="bibr" rid="B39">Frezza (1938</xref>), 
        pero sobre todo, a los de P. Catalano (1974) y F. de Martino (1972-1975).</p>

        <p>Entre los análisis más recientes están el de B. E. Thomason (1991), 
        ...; F. <xref ref-type="bibr" rid="B15">Canali de Rossi (1997</xref>) 
        ... de ocho volúmenes (2005, 2007, 2013, 2014, 2016, 2017 (dos) 
        y 2018). Destacan también las obras de C. 
        <xref ref-type="bibr" rid="B2">Aulliard (2006</xref>) y 
        de E. <xref ref-type="bibr" rid="B58">Torregaray (2005</xref>-2014): 
        la primera es una valiosa síntesis de una ... 
        dirigidas por Ed. 
        <xref ref-type="bibr" rid="B40">Frézouls y A. Jacquemin (1995</xref>) 
        y de Claude <xref ref-type="bibr" rid="B36">Eilers (2009</xref>).</p>
        </body></article>"""
        xml = xml_utils.etree.fromstring(text)
        self.a = Article(xml, "nome")

    def test_any_xref_parent_nodes_returns_two_tuples_for_bibr(self):
        result = self.a.any_xref_parent_nodes
        nodes_p = self.a.tree.findall(".//p")
        nodes_xref = self.a.tree.findall(".//xref")
        tuple1 = nodes_p[0], nodes_xref[:8]
        tuple2 = nodes_p[1], nodes_xref[8:]
        expected = {"bibr": [tuple1, tuple2]}
        self.assertEqual(expected, result)

    def test_any_xref_ranges_returns_empty_dict_because_there_is_no_range(self):
        result = self.a.any_xref_ranges
        expected = {"bibr": []}
        self.assertEqual(expected, result)
