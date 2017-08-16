# coding=utf-8
import os
import shutil

from ...__init__ import _

from ...generics import utils
from ...generics import fs_utils
from ...generics import img_utils
from ...generics import java_xml_utils
from ...generics.reports import html_reports
from ...generics import xml_validators
from . import xml_versions
from ..data import workarea


class PMCPackageMaker(object):

    def __init__(self, wk, article_items, outputs):
        self.wk = wk
        self.article_items = article_items
        self.outputs = outputs

    def make_package(self):
        doit = False

        utils.display_message('\n')
        utils.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        path = None
        for xml_name, doc in self.article_items.items():

            index += 1
            item_label = str(index) + n + ': ' + xml_name
            utils.display_message(item_label)

            scielo_pkgfiles = workarea.PkgArticleFiles(self.wk.scielo_package_path + '/' + xml_name + '.xml')
            pmc_pkgfiles = workarea.PkgArticleFiles(self.wk.pmc_package_path + '/' + xml_name + '.xml')

            doit = PMCPackageItemMaker(
                doc, self.outputs[xml_name],
                scielo_pkgfiles,
                pmc_pkgfiles).make_package()

        if doit and path is not None:
            workarea.PackageFolder(path).zip()

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

    def __init__(self, doc, outputs, scielo_pkgfiles, pmc_pkgfiles):
        self.doc = doc
        self.outputs = outputs
        self.scielo_pkgfiles = scielo_pkgfiles
        self.pmc_pkgfiles = pmc_pkgfiles

    def make_package(self):
        scielo_dtd_files, pmc_dtd_files = xml_versions.identify_dtd_files(self.scielo_pkgfiles.filename)

        if self.doc.journal_id_nlm_ta is None:
            html_reports.save(self.outputs.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
        else:
            java_xml_utils.xml_transform(
                self.scielo_pkgfiles.filename,
                scielo_dtd_files.xsl_output,
                self.pmc_pkgfiles.filename)

            xml_validator = xml_validators.XMLValidator(pmc_dtd_files)
            xml_validator.validate(
                self.pmc_pkgfiles.filename,
                self.outputs.pmc_dtd_report_filename,
                self.outputs.pmc_style_report_filename
                )
            shutil.copyfile(self.pmc_pkgfiles.filename, self.pmc_pkgfiles.filename + '.xml')
            java_xml_utils.xml_transform(
                self.pmc_pkgfiles.filename + '.xml',
                pmc_dtd_files.xsl_output,
                self.pmc_pkgfiles.filename)
            fs_utils.delete_file_or_folder(self.pmc_pkgfiles.filename + '.xml')
            self.add_files_to_pmc_package()
            self.svg2tiff()
            self.evaluate_tiff_images()
            self.replace_href_values()
            self.normalize_pmc_file()
            return True

    def normalize_pmc_file(self):
        content = fs_utils.read_file(self.pmc_pkgfiles.filename)
        if 'mml:math' in content:
            result = []
            n = 0
            math_id = None
            for item in content.replace('<mml:math', '~BREAK~<mml:math').split('~BREAK~'):
                if item.startswith('<mml:math'):
                    n += 1
                    elem = item[:item.find('>')]
                    if ' id="' not in elem:
                        math_id = 'math{}'.format(n)
                        item = item.replace('<mml:math', '<mml:math id="{}"'.format(math_id))
                result.append(item)
            if math_id is not None:
                fs_utils.write_file(self.pmc_pkgfiles.filename, ''.join(result))

    def add_files_to_pmc_package(self):
        errors = []
        if self.doc.language == 'en':
            self.scielo_pkgfiles.copy_files_except_xml(self.pmc_pkgfiles.path)
            for img in self.pmc_pkgfiles.tiff_items:
                error = img_utils.validate_tiff_image_file(self.pmc_pkgfiles.path+'/'+img)
                if error is not None:
                    errors.append(error)
        else:
            self.remove_en_from_filenames()

    def svg2tiff(self):
        for item in self.pmc_pkgfiles.files_except_xml:
            if item.endswith('.svg'):
                img_utils.convert_svg2png(self.pmc_pkgfiles.path + '/' + item)
        for item in self.pmc_pkgfiles.files_except_xml:
            if item.endswith('.png'):
                img_utils.convert_png2tiff(self.pmc_pkgfiles.path + '/' + item)

    def evaluate_tiff_images(self):
        errors = []
        for f in self.pmc_pkgfiles.tiff_items:
            error = img_utils.validate_tiff_image_file(self.pmc_pkgfiles.path+'/'+f)
            if error is not None:
                errors.append(error)
        return errors

    def remove_en_from_filenames(self):
        content = fs_utils.read_file(self.pmc_pkgfiles.filename)
        files = [os.path.splitext(f) for f in self.scielo_pkgfiles.files_except_xml]
        files = [(name, name[:-3], ext) for name, ext in files if name.endswith('-en')]
        for name, new_name, ext in files:
            shutil.copyfile(
                self.scielo_pkgfiles.path + '/' + name+ext,
                self.pmc_pkgfiles.path+'/'+new_name+ext)
            content = content.replace(name+ext, new_name+ext)
        fs_utils.write_file(self.pmc_pkgfiles.filename, content)

    def replace_href_values(self):
        content = fs_utils.read_file(self.pmc_pkgfiles.filename)
        href_items = {href.name_without_extension: href.ext for href in self.doc.href_files}
        for tif in self.pmc_pkgfiles.tiff_names:
            ext = href_items.get(tif)
            if not ext.startswith('.tif'):
                new_name = tif + '.tif'
                if new_name not in self.pmc_pkgfiles.tiff_items:
                    new_name = tif + '.tiff'
                if new_name in self.pmc_pkgfiles.tiff_items:
                    content = content.replace('href="'+href.src+'"', 'href="'+new_name+'"')
        fs_utils.write_file(self.pmc_pkgfiles.filename, content)
