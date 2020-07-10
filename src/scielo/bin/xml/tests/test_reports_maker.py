import tempfile
import shutil
import pathlib
from unittest import TestCase

from prodtools.validations.reports_maker import (
    AssetsInReport,
    BasicAssetsInReport,
    CollectionAssetsInReport,
)


class TestAssetsInReportReturnsCollectionAssetsInReportForRemoteWebsite(TestCase):

    def setUp(self):
        self.data = AssetsInReport(
            "/root/package_path",
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            "https://qa.scielo.br",
        )

    def test_result_path(self):
        self.assertIsNone(self.data.result_path)

    def test_img_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_path)

    def test_report_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/reports/acron/issue_label',
            self.data.report_path)

    def test_img_link(self):
        self.assertEqual(
            'https://qa.scielo.br/img/revistas/acron/issue_label',
            self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual(
            'https://qa.scielo.br/pdf/acron/issue_label',
            self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual(
            'https://qa.scielo.br/reports/acron/issue_label',
            self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            'https://qa.scielo.br/reports/acron/issue_label',
            self.data.report_link)

    def test_serial_report_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.serial_report_path)

    def test_serial_base_xml_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_source',
            self.data.serial_base_xml_path)


class TestAssetsInReportReturnsBasicAssetsInReport(TestCase):

    def setUp(self):
        self.data = AssetsInReport("/root/package_path", "acron", "label")

    def test_result_path(self):
        self.assertEqual('/root', self.data.result_path)

    def test_img_path(self):
        self.assertEqual('/root/package_path', self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual('/root/package_path', self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual('/root/package_path', self.data.xml_path)

    def test_report_path(self):
        self.assertEqual('/root/errors', self.data.report_path)

    def test_img_link(self):
        self.assertEqual('/root/package_path', self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual('/root/package_path', self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual('/root/package_path', self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            '/root/errors', self.data.report_link)


class TestAssetsInReportReturnsCollectionAssetsInReportForNoRemoteWebsite(TestCase):

    def setUp(self):
        self.data = AssetsInReport(
            "/root/package_path",
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            None
        )

    def test_result_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label',
            self.data.result_path)

    def test_img_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_path)

    def test_report_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.report_path)

    def test_img_link(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.report_link)


class TestBasicAssetsInReport(TestCase):

    def setUp(self):
        self.data = BasicAssetsInReport("/root/package_path")

    def test_result_path(self):
        self.assertEqual('/root', self.data.result_path)

    def test_img_path(self):
        self.assertEqual('/root/package_path', self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual('/root/package_path', self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual('/root/package_path', self.data.xml_path)

    def test_report_path(self):
        self.assertEqual('/root/errors', self.data.report_path)

    def test_img_link(self):
        self.assertEqual('/root/package_path', self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual('/root/package_path', self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual('/root/package_path', self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            '/root/errors', self.data.report_link)


class TestCollectionAssetsInReportForNoRemoteWebsite(TestCase):

    def setUp(self):
        self.data = CollectionAssetsInReport(
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            None
        )

    def test_result_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label',
            self.data.result_path)

    def test_img_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_path)

    def test_report_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.report_path)

    def test_img_link(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.report_link)


class TestCollectionAssetsInReportForRemoteWebsite(TestCase):

    def setUp(self):
        self.data = CollectionAssetsInReport(
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            "https://qa.scielo.br",
        )

    def test_result_path(self):
        self.assertIsNone(self.data.result_path)

    def test_img_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/img/revistas/acron/issue_label',
            self.data.img_path)

    def test_pdf_path(self):
        self.assertEqual(
            '/scielo/web/bases/pdf/acron/issue_label',
            self.data.pdf_path)

    def test_xml_path(self):
        self.assertEqual(
            '/scielo/web/bases/xml/acron/issue_label',
            self.data.xml_path)

    def test_report_path(self):
        self.assertEqual(
            '/scielo/web/htdocs/reports/acron/issue_label',
            self.data.report_path)

    def test_img_link(self):
        self.assertEqual(
            'https://qa.scielo.br/img/revistas/acron/issue_label',
            self.data.img_link)

    def test_pdf_link(self):
        self.assertEqual(
            'https://qa.scielo.br/pdf/acron/issue_label',
            self.data.pdf_link)

    def test_xml_link(self):
        self.assertEqual(
            'https://qa.scielo.br/reports/acron/issue_label',
            self.data.xml_link)

    def test_report_link(self):
        self.assertEqual(
            'https://qa.scielo.br/reports/acron/issue_label',
            self.data.report_link)

    def test_serial_report_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_reports',
            self.data.serial_report_path)

    def test_serial_base_xml_path(self):
        self.assertEqual(
            '/scielo/serial_path/acron/issue_label/base_xml/base_source',
            self.data.serial_base_xml_path)


class TestCollectionAssetsInReportValidateSaveReport(TestCase):

    def setUp(self):
        self.serial_path = tempfile.mkdtemp()
        self.web_app_path = tempfile.mkdtemp()
        self.data = CollectionAssetsInReport(
            "acron", "issue_label",
            self.serial_path,
            self.web_app_path,
            "https://qa.scielo.br",
        )

    def tearDown(self):
        self.serial_path = tempfile.mkdtemp()
        self.web_app_path = tempfile.mkdtemp()

    def test_report_path(self):
        expected = str(
            pathlib.Path(self.web_app_path) / 'htdocs/reports/acron/issue_label'
        )
        self.assertEqual(expected, self.data.report_path)

    def test_serial_report_path(self):
        expected = str(
            pathlib.Path(self.serial_path) / 'acron/issue_label/base_xml/base_reports'
        )
        self.assertEqual(expected, self.data.serial_report_path)

    def test_xml_path(self):
        expected = str(
            pathlib.Path(self.web_app_path) / 'bases/xml/acron/issue_label'
        )
        self.assertEqual(expected, self.data.xml_path)

    def test_save_report_saves_in_serial_report_path(self):
        report_text = "<html><body><p>Teste</p></body></html>"
        with tempfile.TemporaryDirectory() as temp_dir_path:
            report_path = pathlib.Path(temp_dir_path) / "report.html"
            report_path.write_text(report_text)
            self.data.save_report(str(report_path))
            path_result = pathlib.Path(self.data.serial_report_path) / "report.html"
            self.assertEqual(path_result.read_text(), report_text)

    def test_save_report_without_converted_xml(self):
        # Garante que dir report_path existe
        pathlib.Path(self.data.report_path).mkdir(parents=True, exist_ok=True)
        # Grava fake report
        report_path = pathlib.Path(self.web_app_path) / "report.html"
        report_path.write_text("<html><body><p>Teste</p></body></html>")
        # Grava fake XML
        temp_dir_path = pathlib.Path(self.data.xml_path)
        temp_dir_path.mkdir(parents=True, exist_ok=True)

        self.data.save_report(str(report_path))
        path_result = pathlib.Path(self.data.report_path) / "doc.xml"
        self.assertFalse(path_result.exists())

    def test_save_report_copy_converted_xml_to_remote(self):
        # Garante que dir report_path existe
        pathlib.Path(self.data.report_path).mkdir(parents=True, exist_ok=True)
        # Grava fake report
        report_path = pathlib.Path(self.web_app_path) / "report.html"
        report_path.write_text("<html><body><p>Teste</p></body></html>")
        # Grava fake XML
        xml_text = "<article><body><p>Teste</p></body></article>"
        temp_dir_path = pathlib.Path(self.data.xml_path)
        temp_dir_path.mkdir(parents=True, exist_ok=True)
        xml_path = temp_dir_path / "doc.xml"
        xml_path.write_text(xml_text)

        self.data.save_report(str(report_path))
        path_result = pathlib.Path(self.data.report_path) / "doc.xml"
        self.assertEqual(path_result.read_text(), xml_text)
