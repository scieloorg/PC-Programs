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
