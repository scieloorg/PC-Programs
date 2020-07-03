from unittest import TestCase


from prodtools.db.serial import (
    IssuePathsInWebsite,
    IssuePathsInSerial,
)


class TestIssuePathsInWebsite(TestCase):

    def setUp(self):
        self.data = IssuePathsInWebsite("/app/web", "acron", "issue")

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


class TestIssuePathsInSerial(TestCase):

    def setUp(self):
        self.data = IssuePathsInSerial(
            "/scielo/serial", "acron", "issue_folder")

    def test_issue_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder",
            self.data.issue_path)

    def test_relative_issue_path(self):
        self.assertEqual(
            "acron/issue_folder",
            self.data.relative_issue_path)

    def test_old_id_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/id",
            self.data.old_id_path)

    def test_id_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base_xml/id",
            self.data.id_path)

    def test_id_filename(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base_xml/id/i.id",
            self.data.id_filename)

    def test_base_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base",
            self.data.base_path)

    def test_markup_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/markup",
            self.data.markup_path)

    def test_body_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/body",
            self.data.body_path)

    def test_windows_base_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/windows",
            self.data.windows_base_path)

    def test_base_xml_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base_xml",
            self.data.base_xml_path)

    def test_base_reports_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base_xml/base_reports",
            self.data.base_reports_path)

    def test_base_source_path(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base_xml/base_source",
            self.data.base_source_path)

    def test_base(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base/issue_folder",
            self.data.base)

    def test_base_filename(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/base/issue_folder.mst",
            self.data.base_filename)

    def test_windows_base(self):
        self.assertEqual(
            "/scielo/serial/acron/issue_folder/windows/issue_folder",
            self.data.windows_base)
