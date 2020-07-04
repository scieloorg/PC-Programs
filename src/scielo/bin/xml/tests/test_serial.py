from unittest import TestCase, mock
from unittest.mock import call


from prodtools.db.serial import (
    IssuePathsInWebsite,
    IssuePathsInSerial,
    WebsiteFiles,
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

    def test_web_htdocs_reports(self):
        self.assertEqual(
            "/app/web/htdocs/reports/acron/issue",
            self.data.web_htdocs_reports)


class TestWebsiteFiles(TestCase):

    def setUp(self):
        self.data = WebsiteFiles("/app/web", "acron", "issue")

    def test_web_path(self):
        self.assertEqual(
            "/app/web",
            self.data.paths.web_path)

    def test_web_bases_pdf(self):
        self.assertEqual(
            "/app/web/bases/pdf/acron/issue",
            self.data.paths.web_bases_pdf)

    def test_web_bases_xml(self):
        self.assertEqual(
            "/app/web/bases/xml/acron/issue",
            self.data.paths.web_bases_xml)

    def test_web_htdocs_img(self):
        self.assertEqual(
            "/app/web/htdocs/img/revistas/acron/issue",
            self.data.paths.web_htdocs_img)

    def test_web_htdocs_img_html(self):
        self.assertEqual(
            "/app/web/htdocs/img/revistas/acron/issue/html",
            self.data.paths.web_htdocs_img_html)

    def test_web_htdocs_reports(self):
        self.assertEqual(
            "/app/web/htdocs/reports/acron/issue",
            self.data.paths.web_htdocs_reports)

    @mock.patch("prodtools.db.serial.os.listdir")
    def test_identify_ex_aop_pdf_files_to_update(self, mock_listdir):
        mock_listdir.return_value = [
            "a01.pdf", "pt_a01.pdf", "en_a01.pdf", "es_a01.pdf",
            "a02.pdf", "pt_a02.pdf", "en_a02.pdf", "es_a02.pdf",
            "a03.pdf", "pt_a03.pdf", "en_a03.pdf", "es_a03.pdf",
            "a11.pdf", "pt_a11.pdf", "en_a11.pdf", "es_a11.pdf",
            "a21.pdf", "pt_a21.pdf", "en_a21.pdf", "es_a21.pdf",
            ]
        expected = [
            ("/app/web/bases/pdf/acron/issue/a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
        ]
        aop_pdf_replacements = {
            'a01': ('acron/2010nahead', 'a01'),
            'a11': ('acron/2018nahead', 'a11'),
            'a21': ('acron/2020nahead', 'a21'),
        }
        result = self.data.identify_ex_aop_pdf_files_to_update(
            aop_pdf_replacements)
        self.assertEqual(expected, result)

    @mock.patch("prodtools.db.serial.shutil.copy")
    @mock.patch("prodtools.db.serial.os.path.isdir")
    def test_update_ex_aop_pdf_files(self, mock_isdir, mock_copy):
        mock_isdir.side_effect = [True] * 12
        param = [
            ("/app/web/bases/pdf/acron/issue/a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a01.pdf",
             "/app/web/bases/pdf/acron/2010nahead"),
            ("/app/web/bases/pdf/acron/issue/a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a11.pdf",
             "/app/web/bases/pdf/acron/2018nahead"),
            ("/app/web/bases/pdf/acron/issue/a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/pt_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/en_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
            ("/app/web/bases/pdf/acron/issue/es_a21.pdf",
             "/app/web/bases/pdf/acron/2020nahead"),
        ]
        self.data.update_ex_aop_pdf_files(param)
        self.assertEqual(
            mock_copy.call_args_list, [
                call(
                    "/app/web/bases/pdf/acron/issue/a01.pdf",
                    "/app/web/bases/pdf/acron/2010nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/pt_a01.pdf",
                    "/app/web/bases/pdf/acron/2010nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/en_a01.pdf",
                    "/app/web/bases/pdf/acron/2010nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/es_a01.pdf",
                    "/app/web/bases/pdf/acron/2010nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/a11.pdf",
                    "/app/web/bases/pdf/acron/2018nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/pt_a11.pdf",
                    "/app/web/bases/pdf/acron/2018nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/en_a11.pdf",
                    "/app/web/bases/pdf/acron/2018nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/es_a11.pdf",
                    "/app/web/bases/pdf/acron/2018nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/a21.pdf",
                    "/app/web/bases/pdf/acron/2020nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/pt_a21.pdf",
                    "/app/web/bases/pdf/acron/2020nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/en_a21.pdf",
                    "/app/web/bases/pdf/acron/2020nahead"),
                call(
                    "/app/web/bases/pdf/acron/issue/es_a21.pdf",
                    "/app/web/bases/pdf/acron/2020nahead")
            ]
        )
        self.assertEqual(
            mock_isdir.call_args_list, [
                call("/app/web/bases/pdf/acron/2010nahead"),
                call("/app/web/bases/pdf/acron/2010nahead"),
                call("/app/web/bases/pdf/acron/2010nahead"),
                call("/app/web/bases/pdf/acron/2010nahead"),
                call("/app/web/bases/pdf/acron/2018nahead"),
                call("/app/web/bases/pdf/acron/2018nahead"),
                call("/app/web/bases/pdf/acron/2018nahead"),
                call("/app/web/bases/pdf/acron/2018nahead"),
                call("/app/web/bases/pdf/acron/2020nahead"),
                call("/app/web/bases/pdf/acron/2020nahead"),
                call("/app/web/bases/pdf/acron/2020nahead"),
                call("/app/web/bases/pdf/acron/2020nahead")
            ]
        )


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
