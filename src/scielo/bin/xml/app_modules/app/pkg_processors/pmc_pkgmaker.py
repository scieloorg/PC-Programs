# coding=utf-8
import os
import shutil

from ...__init__ import _

from ...generics import encoding
from ...generics import fs_utils
from ...generics import java_xml_utils
from ...generics.reports import html_reports
from ..validations import sps_xml_validators
from . import xml_versions
from ..data import workarea
from ..data import package


class PMCPackageMaker(object):

    def __init__(self, wk, article_items, outputs):
        self.wk = wk
        self.article_items = article_items
        self.outputs = outputs

    def make_package(self):
        doit = False

        encoding.display_message('\n')
        encoding.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        fs_utils.delete_file_or_folder(self.wk.pmc_package_path)
        for xml_name, doc in self.article_items.items():
            index += 1
            item_label = str(index) + n + ': ' + xml_name
            encoding.display_message(item_label)

            scielo_pkgfiles = package.ArticlePkg(self.wk.scielo_package_path + '/' + xml_name + '.xml')
            pmc_filename = self.wk.pmc_package_path + '/' + xml_name + '.xml'

            doit = PMCPackageItemMaker(
                self.outputs[xml_name],
                scielo_pkgfiles,
                pmc_filename).make_package()

        if doit:
            workarea.PackageFolder(self.wk.pmc_package_path).zip()

    def make_report(self):
        for xml_name, doc in self.article_items.items():
            msg = _('generating report... ')
            if doc.tree is None:
                msg = _('Unable to generate the XML file. ')
            else:
                if doc.journal_id_nlm_ta is None:
                    msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file. ')
            html_reports.save(self.outputs[xml_name].pmc_style_report_filename, 'PMC Style Checker', msg)


class PMCPackageItemMaker(object):

    def __init__(self, outputs, scielo_pkgfiles, pmc_xml_filename):
        self.outputs = outputs
        self.scielo_pkgfiles = scielo_pkgfiles
        self.pmc_pkgfiles = None
        self.pmc_xml_filename = pmc_xml_filename

    def make_package(self):
        scielo_dtd_files, pmc_dtd_files = xml_versions.identify_dtd_files(self.scielo_pkgfiles.xml_content.content)

        if self.scielo_pkgfiles.article_xml.journal_id_nlm_ta is None:
            html_reports.save(self.outputs.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
        else:
            self.make_xml(scielo_dtd_files, pmc_dtd_files)
            self.pmc_pkgfiles = package.ArticlePkg(self.pmc_xml_filename)
            self.insert_math_id()
            self.replace_img_ext_to_tiff()
            self.add_files_to_pmc_package()
            self.rename_en_files()
            return True

    def make_xml(self, scielo_dtd_files, pmc_dtd_files):
        java_xml_utils.xml_transform(
            self.scielo_pkgfiles.filename,
            scielo_dtd_files.xsl_output,
            self.pmc_xml_filename)
        xml_validator = sps_xml_validators.XMLValidator(pmc_dtd_files)
        xml_validator.validate(
            self.pmc_xml_filename,
            self.outputs.pmc_dtd_report_filename,
            self.outputs.pmc_style_report_filename
            )
        shutil.copyfile(self.pmc_xml_filename, self.pmc_xml_filename + '.xml')
        java_xml_utils.xml_transform(
            self.pmc_xml_filename + '.xml',
            pmc_dtd_files.xsl_output,
            self.pmc_xml_filename)
        fs_utils.delete_file_or_folder(self.pmc_xml_filename + '.xml')

    def insert_math_id(self):
        # PMC exige o atributo @id para math
        xml = self.pmc_pkgfiles.xml_content.xml
        n = 0
        for math in xml.findall("{http://www.w3.org/1998/Math/MathML}math"):
            if math.get("id") is None:
                n += 1
                math.set("id", 'math{}'.format(n))
        if n:
            fs_utils.write_file(self.pmc_xml_filename, xml.content)

    def replace_img_ext_to_tiff(self):
        missing = []
        content = self.pmc_pkgfiles.xml_content.content
        for href in self.pmc_pkgfiles.article_xml.image_files:
            if self.pmc_pkgfiles.related_files_by_extension.get(href.ext) is None:
                missing.append(href.name_without_extension + '.tif')
                content = content.replace(href.src, href.name_without_extension + '.tif')
        self.pmc_pkgfiles.article_xml = content
        #print('missing', missing)

    def add_files_to_pmc_package(self):
        doc = self.pmc_pkgfiles.article_xml
        if doc.language == 'en':
            self.scielo_pkgfiles.copy_related_files(self.pmc_pkgfiles.path)
            self.pmc_pkgfiles.svg2tiff()
            valid_files = self.pmc_pkgfiles.select_pmc_files()
            delete_files = [f for f in self.pmc_pkgfiles.related_files if f not in valid_files]
            self.pmc_pkgfiles.delete_files(delete_files)

    def rename_en_files(self):
        en_files = [f for f in self.pmc_pkgfiles.related_files if '-en.' in f]
        content = self.pmc_pkgfiles.xml_content.content
        for f in en_files:
            new = f.replace('-en.', '.')
            os.rename(self.pmc_pkgfiles.path + '/' + f, self.pmc_pkgfiles.path + '/' + new)
            content = content.replace(f, new)
        if len(en_files) > 0:
            self.pmc_pkgfiles.article_xml = content
            fs_utils.write_file(self.pmc_xml_filename, content)
