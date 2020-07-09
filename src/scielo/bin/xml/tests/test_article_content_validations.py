from unittest import TestCase
from unittest.mock import Mock, PropertyMock
from lxml import etree


from prodtools.validations.article_content_validations import (
    ArticleContentValidation
)
from prodtools.data.article import (
    Article
)


class TestArticleContentValidation(TestCase):

    def setUp(self):
        self.acv = ArticleContentValidation(
            journal=Mock(),
            _article=Mock(),
            pkgfiles=Mock(),
            is_db_generation=Mock(),
            check_url=Mock(),
            doi_validator=Mock(),
            config=Mock()
        )
        self.role_values = ('reviewer', 'reader', 'author', 'editor', )

    def test_validate_peer_review_contrib_anon_retuns_empty_list(self):
        article_type = "DUMMY"
        text = """<article article-type="DUMMY">
            <contrib-group>
                <contrib><anonymous/><role specific-use="{}"/></contrib>
            </contrib-group>
        </article>"""
        for role_value in self.role_values:
            t = text.format(role_value)
            xml = etree.fromstring(t)
            contrib = xml.findall(".//contrib")
            with self.subTest(i=role_value):
                result = self.acv.validate_peer_review_contrib_anon(
                            article_type, 2, contrib[0])
                self.assertEqual(result, [])

    def test_validate_peer_review_contrib_anon_retuns_message_because_of_wrong_value_for_role_specific_use(self):
        article_type = "DUMMY"
        text = """<article article-type="DUMMY">
            <contrib-group>
                <contrib><anonymous/><role specific-use="{}"/></contrib>
            </contrib-group>
        </article>"""
        for role_value in self.role_values:
            t = text.format("wrong-"+role_value)
            xml = etree.fromstring(t)
            contrib = xml.findall(".//contrib")
            with self.subTest(i=role_value):
                result = self.acv.validate_peer_review_contrib_anon(
                            article_type, 2, contrib[0])
                self.assertEqual(
                    result,
                    ['contrib[2] in DUMMY must have "role/@specific-use". '
                     'Expected values: reviewer, reader, author, editor. '])

    def test_validate_peer_review_contrib_anon_retuns_message_of_missing_role_if_no_specific_use_is_set(self):
        article_type = "DUMMY"
        text = """<article article-type="DUMMY">
            <contrib-group>
                <contrib><anonymous/><role/></contrib>
            </contrib-group>
        </article>"""
        xml = etree.fromstring(text)
        contrib = xml.findall(".//contrib")
        result = self.acv.validate_peer_review_contrib_anon(
                    article_type, 2, contrib[0])
        self.assertEqual(
            result,
            ['contrib[2] in DUMMY must have "role/@specific-use". '
             'Expected values: reviewer, reader, author, editor. '])

    def test_validate_peer_review_contrib_anon_retuns_message_of_missing_role(self):
        article_type = "DUMMY"
        text = """<article article-type="DUMMY">
            <contrib-group>
                <contrib><anonymous/></contrib>
            </contrib-group>
        </article>"""
        xml = etree.fromstring(text)
        contrib = xml.findall(".//contrib")
        result = self.acv.validate_peer_review_contrib_anon(
                    article_type, 2, contrib[0])
        self.assertEqual(
            result,
            ['contrib[2] in DUMMY must have "role"'])

    def test_contrib_validation_returns_empty_list_because_it_is_not_required_contrib_for_addendum(
        self,
    ):
        text = """<article 
            xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="addendum" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
        </article>"""

        xml = etree.fromstring(text)
        mk_article = Mock()
        type(mk_article).doc_and_contribs_items = PropertyMock(
            return_value=[(xml, xml.findall(".//contrib"),)]
        )

        content_validation = ArticleContentValidation(
            journal=Mock(),
            _article=mk_article,
            pkgfiles=Mock(),
            is_db_generation=Mock(),
            check_url=Mock(),
            doi_validator=Mock(),
            config=Mock(),
        )

        self.assertEqual(content_validation.contrib, [])


class TestArticleContentValidationRelatedObjects(TestCase):

    def get_article_content_validations(self, xml):
        return ArticleContentValidation(
            journal=Mock(),
            _article=Article(xml, 'xml_name'),
            pkgfiles=Mock(),
            is_db_generation=Mock(),
            check_url=Mock(),
            doi_validator=Mock(),
            config=Mock()
        )

    def test_related_objects_returns_empty_list_if_article_has_no_related_objects(self):
        text = """<article article-type="DUMMY">
            </article>"""
        xml = etree.fromstring(text)
        acv = self.get_article_content_validations(xml)
        result = acv.related_objects
        self.assertEqual([], result)

    def test_related_objects_returns_ok_msg_list_if_related_object_type_is_correct(self):
        text = """<article article-type="DUMMY">
            <front>
            <article-meta>
            <related-object related-object-type="{}"/>
            </article-meta>
            </front>
            </article>"""
        for reltp in ('referee-report', 'peer-reviewed-material', ):
            with self.subTest(reltp):
                xml = etree.fromstring(text.format(reltp))
                acv = self.get_article_content_validations(xml)
                result = acv.related_objects
                expected = [
                    ('related-object/@related-object-type', '[OK]', reltp)]
                self.assertEqual(expected, result)

    def test_related_objects_returns_error_list_if_related_object_type_is_incorrect(self):
        text = """<article article-type="DUMMY">
            <front>
            <article-meta>
            <related-object related-object-type="{}"/>
            </article-meta>
            </front>
            </article>"""
        for reltp in ('xreferee-report', 'xpeer-reviewed-material', ):
            with self.subTest(reltp):
                xml = etree.fromstring(text.format(reltp))
                acv = self.get_article_content_validations(xml)
                result = acv.related_objects
                expected = [
                    ('related-object/@related-object-type',
                        '[FATAL ERROR]',
                        'referee-report | peer-reviewed-material')]

                self.assertEqual(expected[0][0], result[0][0])
                self.assertEqual(expected[0][1], result[0][1])
                self.assertIn(expected[0][2], result[0][2])

    def test_related_objects_returns_ok_msg_list_if_related_object_types_are_correct(self):
        text = """<article article-type="DUMMY">
            <front>
            <article-meta>
            <related-object related-object-type="referee-report"/>
            <related-object related-object-type="referee-report"/>
            </article-meta>
            </front>
            </article>"""
        xml = etree.fromstring(text)
        acv = self.get_article_content_validations(xml)
        result = acv.related_objects
        expected = [
            ('related-object/@related-object-type', '[OK]', 'referee-report'),
            ('related-object/@related-object-type', '[OK]', 'referee-report'),
        ]
        self.assertEqual(expected, result)

    def test_related_objects_returns_ok_and_error_for_related_object_types_correct_and_incorrect(self):
        text = """<article article-type="DUMMY">
            <front>
            <article-meta>
            <related-object related-object-type="xxxreferee-report"/>
            <related-object related-object-type="referee-report"/>
            </article-meta>
            </front>
            </article>"""
        xml = etree.fromstring(text)
        acv = self.get_article_content_validations(xml)
        result = acv.related_objects
        expected = [
            ('related-object/@related-object-type', '[FATAL ERROR]', 'xxxreferee-report'),
            ('related-object/@related-object-type', '[OK]', 'referee-report'),
        ]
        self.assertEqual(expected[0][0], result[0][0])
        self.assertEqual(expected[0][1], result[0][1])
        self.assertIn(expected[0][2], result[0][2])
        self.assertEqual(expected[1], result[1])

    def test_related_objects_returns_error_because_xlink_href_is_not_doi(self):
        text = """<article article-type="DUMMY">
            <front>
            <article-meta>
            <related-object related-object-type="referee-report" ext-link-type= "doi"/>
            </article-meta>
            </front>
            </article>"""
        xml = etree.fromstring(text)
        acv = self.get_article_content_validations(xml)
        result = acv.related_objects
        expected = [
            ('related-object/@related-object-type', '[OK]', 'referee-report'),
            ('related-object/@xlink:href', '[FATAL ERROR]', 'None'),
        ]
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1][0], result[1][0])

    def test_related_objects_returns_OK_because_xlink_href_is_doi(self):
        text = """<article article-type="DUMMY" xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
            <related-object related-object-type="referee-report" ext-link-type="doi" xlink:href="10.1590/abd1806-4841.20142998"/>
            </article-meta>
            </front>
            </article>"""
        xml = etree.fromstring(text)
        acv = self.get_article_content_validations(xml)
        result = acv.related_objects
        expected = [
            ('related-object/@related-object-type', '[OK]', 'referee-report'),
        ]
        self.assertEqual(expected, result)


class TestArticleContentValidationXref(TestCase):

    def get_article_content_validations(self, text):
        xml = etree.fromstring(text)
        return ArticleContentValidation(
            journal=Mock(),
            _article=Article(xml, 'xml_name'),
            pkgfiles=Mock(),
            is_db_generation=Mock(),
            check_url=Mock(),
            doi_validator=Mock(),
            config=Mock()
        )

    def test_missing_xref_returns_empty_list(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B01">1</xref>'
            '-<xref ref-type="bibr" rid="B02">2</xref>'
            '</p></body>'
            '<back>'
            '<ref-list>'
            '</ref-list>'
            '</back>'
            '</article>'
        )
        acv = self.get_article_content_validations(text)
        result = acv.missing_xref_list
        expected = []
        self.assertEqual(expected, result)

    def test_missing_xref_returns_error(self):
        text = (
            '<article>'
            '<body><p>'
            '<xref ref-type="bibr" rid="B03">3</xref>'
            '-<xref ref-type="bibr" rid="B02">2</xref>'
            '</p></body>'
            '<back>'
            '<ref-list>'
            '</ref-list>'
            '</back>'
            '</article>'
        )
        acv = self.get_article_content_validations(text)
        result = acv.missing_xref_list
        self.assertEqual("[ERROR]", result[0][1])
        self.assertIn("3-2 (B03-B02)", result[0][2])

    def test_missing_xref_returns_empty_list_because_there_is_not_range(self):
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
        acv = self.get_article_content_validations(text)
        result = acv.missing_xref_list
        expected = []
        self.assertEqual(expected, result)
