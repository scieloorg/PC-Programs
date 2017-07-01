# coding=utf-8

from ..__init__ import _

from ..utils import utils
from ..utils import fs_utils
from ..utils import img_utils
from ..utils import xml_utils
from ..reports import html_reports
from ..data import workarea
from ..validations import xml_validators
from . import xml_versions


class PMCPackageMaker(object):

    def __init__(self, version):
        self.pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
        self.scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    def make_package(self, article_items, workareas):
        doit = False

        utils.display_message('\n')
        utils.display_message(_('Generating PMC Package'))
        n = '/' + str(len(article_items))
        index = 0

        path = None
        for xml_name, doc in article_items.keys():
            wk = workareas[xml_name]
            path = wk.pmc_pkgfiles.path

            index += 1
            item_label = str(index) + n + ': ' + xml_name
            utils.display_message(item_label)

            doit = PMCPackageItemMaker(doc, wk, self.scielo_dtd_files, self.pmc_dtd_files).make_package()

        if doit and path is not None:
            workarea.PackageFolder(path).zip()

    def make_report(self, article_items, workareas):
        for xml_name, doc in article_items.items():
            msg = _('generating report... ')
            if doc.tree is None:
                msg = _('Unable to generate the XML file. ')
            else:
                if doc.journal_id_nlm_ta is None:
                    msg = _('It is not PMC article or unable to find journal-id (nlm-ta) in the XML file. ')
            html_reports.save(workareas[xml_name].pmc_style_report_filename, 'PMC Style Checker', msg)


class PMCPackageItemMaker(object):

    def __init__(self, doc, wk, scielo_dtd_files, pmc_dtd_files):
        self.doc = doc
        self.wk = wk
        self.pmc_dtd_files = pmc_dtd_files
        self.scielo_dtd_files = scielo_dtd_files
        self.pmc_xml_filename = wk.pmc_pkgfiles.filename
        self.scielo_xml_filename = wk.scielo_pkgfiles.filename
        self.pmc_style_report_filename = self.wk.outputs.pmc_style_report_filename

    def make_package(self):
        if self.doc.journal_id_nlm_ta is None:
            html_reports.save(self.pmc_style_report_filename, 'PMC Style Checker', _('{label} is a mandatory data, and it was not informed. ').format(label='journal-id (nlm-ta)'))
        else:
            xml_output(
                self.scielo_xml_filename,
                self.scielo_dtd_files.doctype_with_local_path,
                self.scielo_dtd_files.xsl_output,
                self.pmc_xml_filename)

            xml_validator = xml_validators.XMLValidator(self.pmc_dtd_files)
            xml_validator.validate_style(
                self.pmc_xml_filename,
                self.pmc_style_report_filename
                )

            xml_output(self.pmc_xml_filename,
                self.pmc_dtd_files.doctype_with_local_path,
                self.pmc_dtd_files.xsl_output,
                self.pmc_xml_filename)

            self.add_files_to_pmc_package()
            self.svg2tiff()
            self.evaluate_tiff_images()
            self.replace_href_values()
            self.normalize_pmc_file()
            return True

    def normalize_pmc_file(self):
        content = fs_utils.read_file(self.pmc_xml_filename)
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
                        print(math_id)
                result.append(item)
            if math_id is not None:
                fs_utils.write_file(self.pmc_xml_filename, ''.join(result))

    def add_files_to_pmc_package(self):
        errors = []
        if self.doc.language == 'en':
            self.wk.scielo_pkgfiles.copy(self.wk.pmc_pkgfiles.path)
            for img in self.wk.pmc_pkgfiles.tiff_items:
                error = img_utils.validate_tiff_image_file(self.wk.pmc_pkgfiles.path+'/'+img)
                if error is not None:
                    errors.append(error)
        else:
            self.remove_en_from_filenames(self)

    def svg2tiff(self):
        for item in self.wk.pmc_pkgfiles.files_except_xml:
            if item.endswith('.svg'):
                img_utils.convert_svg2png(self.wk.pmc_pkgfiles.path + '/' + item)
        for item in self.wk.pmc_pkgfiles.files_except_xml:
            if item.endswith('.png'):
                img_utils.convert_png2tiff(self.wk.pmc_pkgfiles.path + '/' + item)

    def evaluate_tiff_images(self):
        errors = []
        for f in self.wk.pmc_pkgfiles.tiff_items:
            error = img_utils.validate_tiff_image_file(self.wk.pmc_pkgfiles.path+'/'+f)
            if error is not None:
                errors.append(error)
        return errors

    def remove_en_from_filenames(self):
        content = fs_utils.read_file(self.wk.pmc_pkgfiles.filename)
        files = [os.path.splitext(f) for f in self.wk.scielo_pkgfiles.files_except_xml]
        files = [(name, name[:-3], ext) for name, ext in files if name.endswith('-en')]
        for name, new_name, ext in files:
            shutil.copyfile(
                self.wk.scielo_pkgfiles.path + '/' + name+ext,
                self.wk.pmc_pkgfiles.path+'/'+new_name+ext)
            content = content.replace(name+ext, new_name+ext)
        fs_utils.write_file(self.pmc_xml_filename, content)

    def replace_href_values(self):
        content = fs_utils.read_file(self.wk.pmc_pkgfiles.filename)
        href_items = {href.name_with_extension: href.ext for href in self.doc.href_files}
        for tif in self.wk.pmc_pkgfiles.tiff_names:
            ext = href_items.get(tif)
            if not ext.startswith('.tif'):
                new_name = tif + '.tif'
                if not new_name in self.wk.pmc_pkgfiles.tiff_items:
                    new_name = tif + '.tiff'
                if new_name in self.wk.pmc_pkgfiles.tiff_items:
                    content = content.replace('href="'+href.src+'"', 'href="'+new_name+'"')
                    print(href.src, new_name)
        fs_utils.write_file(self.pmc_xml_filename, content)


def xml_output(xml_filename, doctype, xsl_filename, result_filename):
    #FIXME
    if result_filename == xml_filename:
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        xml_filename = xml_filename + '.bkp'

    fs_utils.delete_file_or_folder(result_filename)

    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    r = java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)

    if not result_filename == xml_filename:
        xml_utils.restore_xml_file(xml_filename, bkp_xml_filename)
    if xml_filename.endswith('.bkp'):
        fs_utils.delete_file_or_folder(xml_filename)
    return r
