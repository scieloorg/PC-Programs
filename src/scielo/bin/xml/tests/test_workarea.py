from unittest import TestCase

from prodtools.data.workarea import (
    AssetsDestinations,
    BasicAssetsDestinations,
    CollectionAssetsDestinations,
)



class TestAssetsDestinationsReturnsCollectionAssetsDestinationsForRemoteWebsite(TestCase):

    def setUp(self):
        self.data = AssetsDestinations(
            "/root/package_path",
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            "https://qa.scielo.br",
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


class TestAssetsDestinationsReturnsBasicAssetsDestinations(TestCase):

    def setUp(self):
        self.data = AssetsDestinations("/root/package_path", "acron", "label")

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


class TestAssetsDestinationsReturnsCollectionAssetsDestinationsForNoRemoteWebsite(TestCase):

    def setUp(self):
        self.data = AssetsDestinations(
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


class TestBasicAssetsDestinations(TestCase):

    def setUp(self):
        self.data = BasicAssetsDestinations("/root/package_path")

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


class TestCollectionAssetsDestinationsForNoRemoteWebsite(TestCase):

    def setUp(self):
        self.data = CollectionAssetsDestinations(
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


class TestCollectionAssetsDestinationsForRemoteWebsite(TestCase):

    def setUp(self):
        self.data = CollectionAssetsDestinations(
            "/root/package_path",
            "acron", "issue_label",
            "/scielo/serial_path",
            "/scielo/web",
            "https://qa.scielo.br",
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
