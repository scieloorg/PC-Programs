# coding=utf-8
import logging
import logging.config
import os
import shutil

from ...generics import fs_utils
from ...generics import img_utils


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


MARKUP_SUFFIXES = ['t', 'f', 'e', 'img', 'image']
MARKUP_SUFFIXES.extend(['-'+s for s in MARKUP_SUFFIXES])
MARKUP_SUFFIXES.extend(['-', '.', '0'])

XML_SUFFIXES = ['-', '.']


class File(object):

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)


class MultiDocsPackageOuputs(object):

    def __init__(self, output_path):
        self.output_path = output_path
        for p in [self.reports_path, self.tmp_path,
                  self.scielo_package_path, self.pmc_package_path]:
            if not os.path.isdir(p):
                os.makedirs(p)
        self.doc_outs = {}

    @property
    def reports_path(self):
        return os.path.join(self.output_path, 'errors')

    @property
    def tmp_path(self):
        return os.path.join(self.output_path, 'tmp')

    @property
    def scielo_package_path(self):
        return os.path.join(self.output_path, 'scielo_package')

    @property
    def pmc_package_path(self):
        return os.path.join(self.output_path, 'pmc_package')

    def get_doc_outputs(self, xml_name, sgmxml_name=None):
        obj = self.doc_outs.get(xml_name)
        if obj is None:
            if sgmxml_name:
                work_path = os.path.join(self.output_path, "work", sgmxml_name)
            else:
                work_path = os.path.join(self.tmp_path, xml_name)
            self.doc_outs[xml_name] = DocumentOutputFiles(
                xml_name, self.reports_path, work_path)
            obj = self.doc_outs[xml_name]
        return obj


class DocumentPackageFiles(object):

    def __init__(self, filename):
        self._prefixes = None
        self.filename = filename
        self.path = os.path.dirname(filename)
        self.is_mkp = self.filename.endswith('.sgm.xml') or self.path.endswith('src')
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)

        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        self.folder = os.path.basename(self.path)
        if self.filename.endswith('.sgm.xml'):
            self.name, ign = os.path.splitext(self.name)
        self.previous_name = self.name
        self.listdir = []
        self._load()

    def add_extension(self, new_href):
        if '.' not in new_href:
            extensions = self.related_files_by_name.get(new_href)
            if extensions is not None:
                if len(extensions) > 1:
                    extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
                if len(extensions) > 0:
                    new_href += extensions[0]
        return new_href

    @property
    def prefixes(self):
        if self._prefixes is None:
            r = []
            SUFFIXES = XML_SUFFIXES
            if self.is_mkp:
                SUFFIXES = MARKUP_SUFFIXES
                if self.basename.startswith('a') and self.basename[3:4] == 'v':
                    r.extend([self.basename[:3] + suffix for suffix in SUFFIXES])
            r.extend([self.name + suffix for suffix in SUFFIXES])
            self._prefixes = list(set(r))
        return self._prefixes

    def find_files(self):
        r = []
        files = [item
                 for item in self.listdir
                 if (os.path.isfile(os.path.join(self.path, item)) and
                     not item.endswith('incorrect.xml') and
                     not item.endswith('.sgm.xml'))]
        for item in files:
            selected = [item for prefix in self.prefixes if item.startswith(prefix)]
            r.extend(selected)
        return list(set(r))

    def is_listdir_changed(self):
        listdir = os.listdir(self.path)
        if set(listdir) != set(self.listdir):
            self.listdir = listdir
            return True
        return False

    def _update(self):
        if self.is_listdir_changed():
            self._load()

    def _load(self):
        self._files = self.find_files()
        self._related_files = [f for f in self.files if f != self.basename and not f.endswith('.ctrl.txt')]
        self._related_files_by_name = {}
        self._related_files_by_extension = {}
        for f in self._related_files:
            name, extension = os.path.splitext(f)
            if name not in self._related_files_by_name.keys():
                self._related_files_by_name[name] = []
            if extension not in self._related_files_by_extension.keys():
                self._related_files_by_extension[extension] = []
            if extension not in self._related_files_by_name[name]:
                self._related_files_by_name[name].append(extension)
            if name not in self._related_files_by_extension[extension]:
                self._related_files_by_extension[extension].append(name)

    @property
    def files(self):
        self._update()
        return self._files

    @property
    def related_files(self):
        self._update()
        return self._related_files

    @property
    def related_files_by_name(self):
        self._update()
        return self._related_files_by_name

    @property
    def related_files_by_extension(self):
        self._update()
        return self._related_files_by_extension

    def files_by_ext(self, extensions):
        r = []
        for ext in extensions:
            r.extend([name+ext for name in self.related_files_by_extension.get(ext, [])])
        return r

    @property
    def png_items(self):
        return self.files_by_ext(['.png'])

    @property
    def jpg_items(self):
        return self.files_by_ext(['.jpg', '.jpeg'])

    @property
    def tiff_items(self):
        return self.files_by_ext(['.tif', '.tiff'])

    @property
    def png_names(self):
        return self.related_files_by_extension.get('.png', [])

    @property
    def jpg_names(self):
        return self.related_files_by_extension.get('.jpg', []) + self.related_files_by_extension.get('.jpeg', [])

    @property
    def tiff_names(self):
        return self.related_files_by_extension.get('.tiff', []) + self.related_files_by_extension.get('.tif', [])

    def clean(self):
        for f in self.related_files:
            fs_utils.delete_file_or_folder(os.path.join(self.path, f))
        self._update()

    # def tiff2jpg(self):
    #     for item in self.tiff_names:
    #         if item not in self.jpg_names and item not in self.png_names:
    #             source_fname = item + '.tif'
    #             if source_fname not in self.related_files:
    #                 source_fname = item + '.tiff'
    #             img_utils.hdimg_to_jpg(self.path + '/' + source_fname, self.path + '/' + item + '.jpg')
    #     self._update()

    def delete_files(self, files):
        for f in files:
            fs_utils.delete_file_or_folder(os.path.join(self.path, f))
        self._update()

    def svg2tiff(self):
        sgv2png_files = None
        png2tiff_files = None
        if len(self.tiff_items) == 0:
            sgv2png_files = img_utils.svg2png(self.path)
            self._update()
            png2tiff_files = img_utils.png2tiff(self.path)
            self._update()
        return sgv2png_files, png2tiff_files

    @property
    def tiff_name_and_basename_items(self):
        items = []
        for item in self.tiff_items:
            name, ext = os.path.splitext(item)
            items.append((name, item))
        return dict(items)

    def created_tiff_img_files_from_other_formats(self):
        svg2png_files, png2tiff_files = self.svg2tiff()
        svg2png_files = dict(svg2png_files or {})
        png2tiff_files = dict(png2tiff_files or {})
        replace = {}
        for k, k_in_png2tiff in svg2png_files.items():
            if png2tiff_files.get(k_in_png2tiff):
                replace[os.path.basename(k)] = os.path.basename(
                    png2tiff_files.pop(k_in_png2tiff))
        replace.update(
            {os.path.basename(k): os.path.basename(v)
             for k, v in png2tiff_files.items()
             }
        )
        return replace

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        filename = os.path.join(dest_path, self.name + '.zip')
        fs_utils.zip(
            filename, [os.path.join(self.path, f) for f in self.files])
        return filename

    def copy_related_files(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            for f in self.related_files:
                shutil.copyfile(
                    os.path.join(self.path, f), os.path.join(dest_path, f))

    def copy_xml(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            shutil.copyfile(
                self.filename, os.path.join(dest_path, self.basename))

    def match_img_files_by_suffixes(self, suffixes):
        found = []
        for f in self.files:
            f_name, f_ext = os.path.splitext(f)
            if f_ext in img_utils.IMG_EXTENSIONS:
                suffix = f_name[len(self.name):]
                if suffix in suffixes:
                    found.append(f)
        return found

    def match_img_files_by_id(self, elem_id):
        found = []
        for f in self.files:
            f_name, f_ext = os.path.splitext(f)
            if f_ext in img_utils.IMG_EXTENSIONS:
                suffix = f_name[len(self.name):]
                if suffix == elem_id:
                    found.append(f)
        return found

    def search_files(self, number, elem_id, suffixes):
        if number:
            found = self.match_img_files_by_suffixes(suffixes)
        else:
            found = self.match_img_files_by_id(elem_id)
        return found


class MultiDocsPackageFolder(object):

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.pkgfiles_items = {}
        for item in os.listdir(path):
            if item.endswith('.xml'):
                logger.info("Package Item: %s" % (os.path.join(path, item)))
                article_files = DocumentPackageFiles(os.path.join(path, item))
                self.pkgfiles_items[article_files.name] = article_files
        self.INFORM_ORPHANS = len(self.pkgfiles_items) > 1

    @property
    def prefix(self):
        if len(self.pkgfiles_items) > 0:
            name = list(self.pkgfiles_items.keys())[0].split("-")
            return "-".join(name[:-1])

    @property
    def xml_list(self):
        return [item.filename for item in self.pkgfiles_items.values()]

    @property
    def file_paths(self):
        return {name: item.filename
                for name, item in self.pkgfiles_items.items()}

    @property
    def package_filenames(self):
        items = []
        for pkg in self.pkgfiles_items.values():
            items.extend(pkg.files)
        return items

    @property
    def orphans(self):
        items = []
        if self.INFORM_ORPHANS is True:
            for f in os.listdir(self.path):
                if f not in self.package_filenames:
                    items.append(f)
        return items

    def zip(self, dest_path=None):
        dest_path = dest_path or self.path + ".zip"
        if dest_path.endswith(".zip"):
            dirname = os.path.dirname(dest_path)
            dest_name = os.path.basename(dest_path)
            filename = dest_path
        else:
            dirname = dest_path
            dest_name = self.name + '.zip'
            filename = os.path.join(dirname, dest_name)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if os.path.isfile(filename):
            os.unlink(filename)
        fs_utils.zip(filename,
                     [os.path.join(self.path, f)
                      for f in self.package_filenames])
        return filename


class DocumentOutputFiles(object):

    def __init__(self, xml_name, report_path, wrk_path):
        self.xml_name = xml_name
        self.report_path = report_path
        self.wrk_path = wrk_path

    def create_dir_at_work_path(self, dirname):
        dirname = os.path.join(self.wrk_path, dirname)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return dirname

    @property
    def report_path(self):
        return self._report_path

    @report_path.setter
    def report_path(self, _report_path):
        if not os.path.isdir(_report_path):
            os.makedirs(_report_path)
        self._report_path = _report_path

    @property
    def ctrl_filename(self):
        # deve existir apenas na conversao de sgml para xml
        name = os.path.basename(self.wrk_path)
        if name != self.xml_name:
            return os.path.join(self.wrk_path, name + ".ctrl.txt")

    @property
    def style_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.rep.html')

    @property
    def dtd_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.dtd.txt')

    @property
    def pmc_dtd_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.pmc.dtd.txt')

    @property
    def pmc_style_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.pmc.rep.html')

    @property
    def err_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.err.txt')

    @property
    def err_filename_html(self):
        return os.path.join(self.report_path, self.xml_name + '.err.html')

    @property
    def mkp2xml_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.mkp2xml.txt')

    @property
    def mkp2xml_report_filename_html(self):
        return os.path.join(self.report_path, self.xml_name + '.mkp2xml.html')

    @property
    def data_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.contents.html')

    @property
    def images_report_filename(self):
        return os.path.join(self.report_path, self.xml_name + '.images.html')

    @property
    def xml_structure_validations_filename(self):
        return os.path.join(self.report_path, 'xmlstr-' + self.xml_name)

    @property
    def xml_content_validations_filename(self):
        return os.path.join(self.report_path, 'xmlcon-' + self.xml_name)

    @property
    def journal_validations_filename(self):
        return os.path.join(self.report_path, 'journal-' + self.xml_name)

    @property
    def issue_validations_filename(self):
        return os.path.join(self.report_path, 'issue-' + self.xml_name)

    def clean(self):
        for f in [self.err_filename, self.dtd_report_filename,
                  self.style_report_filename, self.pmc_dtd_report_filename,
                  self.pmc_style_report_filename, self.ctrl_filename]:
            fs_utils.delete_file_or_folder(f)


class AssetsDestinations(object):

    def __init__(self, pkg_path, acron, issue_label,
                 serial_path=None, web_app_path=None, web_url=None):
        self.pkg_path = pkg_path
        self.acron = acron
        self.issue_label = issue_label
        self.serial_path = serial_path
        self.web_app_path = web_app_path
        self.web_url = web_url

        self.issue_path = os.path.join(acron, issue_label)

        self._img_revistas_subdir = os.path.join(
            'img', 'revistas', self.issue_path)
        self._pdf_subdir = os.path.join('pdf', self.issue_path)
        self._xml_subdir = os.path.join('xml', self.issue_path)
        self._reports_subdir = os.path.join('reports', self.issue_path)

    @property
    def serial_issue_path(self):
        if self.serial_path:
            return os.path.join(self.serial_path, self.issue_path)

    @property
    def result_path(self):
        if self.serial_issue_path:
            return self.serial_issue_path
        return os.path.dirname(self.pkg_path)

    @property
    def web_bases_path(self):
        if self.web_app_path:
            return os.path.join(self.web_app_path, "bases")

    @property
    def img_path(self):
        if self.web_bases_path:
            return os.path.join(self.web_bases_path, self._img_revistas_subdir)
        return self.pkg_path

    @property
    def pdf_path(self):
        if self.web_bases_path:
            return os.path.join(self.web_bases_path, self._pdf_subdir)
        return self.pkg_path

    @property
    def xml_path(self):
        if self.web_bases_path:
            return os.path.join(self.web_bases_path, self._xml_subdir)
        elif self.serial_issue_path:
            return os.path.join(
                self.serial_issue_path, 'base_xml', 'base_source')
        return self.pkg_path

    @property
    def report_path(self):
        if self.web_app_path:
            return os.path.join(
                self.web_app_path, 'htdocs', self._reports_subdir)
        return os.path.join(self.result_path, 'errors')

    @property
    def report_link(self):
        if self.web_url:
            return os.path.join(self.web_url, self._reports_subdir)
        return os.path.join(self.result_path, 'errors')

    @property
    def base_report_path(self):
        if self.serial_path:
            return os.path.join(
                self.serial_issue_path, 'base_xml', 'base_reports')

    @property
    def img_link(self):
        if self.web_url:
            return os.path.join(self.web_url, self._img_revistas_subdir)
        return os.path.join('file://', self.img_path)

    @property
    def pdf_link(self):
        if self.web_url:
            return os.path.join(self.web_url, self._pdf_subdir)
        return os.path.join('file://', self.pdf_path)

    @property
    def xml_link(self):
        if self.web_url:
            return os.path.join(self.web_url, self._xml_subdir)
        return os.path.join('file://', self.xml_path)
