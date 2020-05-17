# coding=utf-8
import os

from ...__init__ import _

from ...generics import encoding
from ...generics import fs_utils
from ...generics import xml_utils
from ...generics.reports import html_reports
from ..validations import sps_xml_validators
from . import xml_versions
from ..data import workarea


class PMCPackageMaker(object):

    def __init__(self, pkg):
        self.wk = pkg.wk
        self.article_items = pkg.articles
        self.outputs = pkg.outputs
        self.pkg_files = pkg.files

    def make_package(self):
        doit = False

        encoding.display_message('\n')
        encoding.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        for xml_name, doc in self.article_items.items():
            index += 1
            item_label = str(index) + n + ': ' + xml_name
            encoding.display_message(item_label)

            pmc_filename = os.path.join(
                self.wk.pmc_package_path, xml_name + '.xml')

            doit = PMCPackageItemMaker(
                self.outputs[xml_name],
                self.pkg_files[xml_name],
                self.article_items[xml_name],
                pmc_filename).make_package()

        if doit:
            workarea.MultiDocsPackageFolder(self.wk.pmc_package_path).zip()


class PMCPackageItemMaker(object):

    def __init__(self, outputs, scielo_pkg_files, article, pmc_xml_filepath):
        self.outputs = outputs
        self.scielo_pkg_files = scielo_pkg_files
        self.article = article
        self.pmc_pkg_files = None
        self.pmc_xml_filepath = pmc_xml_filepath

    def make_package(self):
        scielo_dtd_files = xml_versions.dtd_files(
            self.article.sps_version_number)
        pmc_dtd_files = xml_versions.dtd_files(
            self.article.sps_version_number, database="pmc")

        if self.article.journal_id_nlm_ta is None:
            html_reports.save(
                self.outputs.pmc_style_report_filename, 'PMC Style Checker',
                _('{label} is a mandatory data, and it was not informed. '
                  ).format(label='journal-id (nlm-ta)'))
        else:
            self.make_xml(scielo_dtd_files, pmc_dtd_files)
            return True

    def make_xml(self, scielo_dtd_files, pmc_dtd_files):
        xml_obj = self.article.tree
        # j1.1/xsl/sgml2xml/xml2pmc.xsl
        xsl_obj = xml_utils.get_xsl_object(scielo_dtd_files.xsl_output)
        result = xml_utils.transform(xml_obj, xsl_obj)
        xml_utils.write(self.pmc_xml_filepath, result)

        self.pmc_pkg_files = workarea.DocumentPackageFiles(
            self.pmc_xml_filepath)
        self._insert_math_id()
        self._add_files_to_pmc_package()
        self._rename_en_files()

        # validate
        xml_validator = sps_xml_validators.PMCXMLValidator(pmc_dtd_files)
        xml_validator.validate(
            self.pmc_xml_filepath,
            self.outputs.pmc_dtd_report_filename,
            self.outputs.pmc_style_report_filename
            )
        # j1.1/xsl/sgml2xml/pmc.xsl
        xsl_obj = xml_utils.get_xsl_object(pmc_dtd_files.xsl_output)
        result = xml_utils.transform(xml_obj, xsl_obj)
        xml_utils.write(self.pmc_xml_filepath, result)

    def _insert_math_id(self):
        # PMC exige o atributo @id para math
        xml = xml_utils.SuitableXML(self.pmc_xml_filepath)
        n = 0
        for math in xml.xml.findall(
                "{http://www.w3.org/1998/Math/MathML}math"):
            if math.get("id") is None:
                n += 1
                math.set("id", 'math{}'.format(n))
        if n:
            xml.write_file(self.pmc_xml_filepath, pretty_print=True)

    def _add_files_to_pmc_package(self):
        if self.article.language == 'en':
            self.scielo_pkg_files.copy_related_files(self.pmc_pkg_files.path)
            self.pmc_pkg_files.svg2tiff()
            valid_files = self.pmc_pkg_files.select_pmc_files()
            delete_files = [f
                            for f in self.pmc_pkg_files.related_files
                            if f not in valid_files]
            self.pmc_pkg_files.delete_files(delete_files)

    def _rename_en_files(self):
        en_files = [f for f in self.pmc_pkg_files.related_files if '-en.' in f]
        xml_obj = xml_utils.SuitableXML(self.pmc_xml_filepath)
        content = xml_obj.content
        for f in en_files:
            new = f.replace('-en.', '.')
            os.rename(os.path.join(self.pmc_pkg_files.path, f),
                      os.path.join(self.pmc_pkg_files.path, new))
            content = content.replace(f, new)
        if len(en_files) > 0:
            xml_obj.content = content
            xml_obj.write_file(self.pmc_xml_filepath, pretty_print=True)
