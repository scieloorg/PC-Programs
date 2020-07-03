from unittest import TestCase


from prodtools.db.serial import (
    WebsiteAssetsLocations,
#    SerialAssetsLocations,
)


class TestWebsiteAssetsLocations(TestCase):

    def setUp(self):
        self.data = WebsiteAssetsLocations("/app/web", "acron", "issue")

    def test_web_path(self):
        self.assertEqual(
            "/app/web",
            self.data.web_path)

    def test_web_bases_pdf(self):
        self.assertEqual(
            "/app/web/bases/pdf/acron/issue",
            self.data.web_bases_pdf)

    def test_web_bases_xml(self):
        self.assertEqual(
            "/app/web/bases/xml/acron/issue",
            self.data.web_bases_xml)

    def test_web_htdocs_img(self):
        self.assertEqual(
            "/app/web/htdocs/img/revistas/acron/issue",
            self.data.web_htdocs_img)

    def test_web_htdocs_img_html(self):
        self.assertEqual(
            "/app/web/htdocs/img/revistas/acron/issue/html",
            self.data.web_htdocs_img_html)

