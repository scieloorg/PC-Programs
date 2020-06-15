from unittest import (
    TestCase,
)
from unittest.mock import (
    Mock,
)
from lxml import etree


from prodtools.validations.article_content_validations import (
    ArticleContentValidation
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
