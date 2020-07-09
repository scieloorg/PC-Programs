from unittest import TestCase

from lxml import etree
from prodtools.data.article import ContribXML


class TestContribXML(TestCase):

    def create(self, text):
        xml = etree.fromstring(text)
        return ContribXML(xml)

    def test_contrib_xml_returns_person_author_xref_is_a01(self):
        text = """
        <contrib xmlns:mml="http://www.w3.org/1998/Math/MathML"
          xmlns:xlink="http://www.w3.org/1999/xlink" contrib-type="author">
          <contrib-id contrib-id-type="orcid">0000-0002-1709-3448</contrib-id>
          <name>
            <surname>Salvalaggio</surname>
            <given-names>Adriana Cologni</given-names>
          </name>
          <xref ref-type="aff" rid="a01">
            <sup>1</sup>
          </xref>
        </contrib>
        """
        expected = ["a01"]
        c = self.create(text)
        result = c.contrib().xref
        self.assertEqual(expected, result)

    def test_contrib_xml_returns_person_author_xref_is_empty_list(self):
        text = """
        <contrib xmlns:mml="http://www.w3.org/1998/Math/MathML"
          xmlns:xlink="http://www.w3.org/1999/xlink" contrib-type="author">
          <contrib-id contrib-id-type="orcid">0000-0002-1709-3448</contrib-id>
          <name>
            <surname>Salvalaggio</surname>
            <given-names>Adriana Cologni</given-names>
          </name>
          <xref ref-type="aff">
            <sup>1</sup>
          </xref>
        </contrib>
        """
        expected = []
        c = self.create(text)
        result = c.contrib().xref
        self.assertEqual(expected, result)
