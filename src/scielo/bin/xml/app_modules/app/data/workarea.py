# coding=utf-8

import os
import shutil

from ...generics import fs_utils
from ...generics import img_utils


SUFFIXES = ['t', 'f', 'e', 'img', 'image']
SUFFIXES.extend(['-'+s for s in SUFFIXES])
SUFFIXES.extend(['-', '.', '0'])


class Workarea(object):

    def __init__(self, output_path):
        self.output_path = output_path

        for p in [self.output_path, self.reports_path, self.scielo_package_path, self.pmc_package_path]:
            if not os.path.isdir(p):
                os.makedirs(p)

    @property
    def reports_path(self):
        return self.output_path + '/errors'

    @property
    def scielo_package_path(self):
        return self.output_path + '/scielo_package'

    @property
    def pmc_package_path(self):
        return self.output_path+'/pmc_package'


class PkgArticleFiles(object):

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.folder = os.path.basename(self.path)
        self.name, self.ext = os.path.splitext(self.basename)
        if self.filename.endswith('.sgm.xml'):
            self.name, ign = os.path.splitext(self.name)
        self.previous_name = self.name
        self._all = None
        self._prefixes = None

    def add_extension(self, new_href):
        if '.' not in new_href:
            extensions = self.files_by_name_except_xml.get(new_href)
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
            if self.folder.endswith('_package'):
                self._prefixes = [self.name + '-', self.name + '.', ]
            else:
                if self.basename.startswith('a') and self.basename[3:4] == 'v':
                    r.append(self.basename[:3])
                r.extend([self.name + suffix for suffix in SUFFIXES])
                self._prefixes = list(set(r))
        return self._prefixes

    def find_all_files(self):
        r = []
        for item in os.listdir(self.path):
            if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml'):
                for prefix in self.prefixes:
                    if item.startswith(prefix):
                        r.append(item)
        self._all = list(set(r))

    @property
    def all(self):
        self.find_all_files()
        return self._all

    @property
    def files_except_xml(self):
        return [f for f in self.all if f != self.basename and not f.endswith('.ctrl.txt')]

    @property
    def files_by_name_except_xml(self):
        files = {}
        for f in self.files_except_xml:
            name, ext = os.path.splitext(f)
            if name not in files.keys():
                files[name] = []
            files[name].append(ext)
        return files

    def clean(self):
        for f in self.files_except_xml:
            fs_utils.delete_file_or_folder(self.path + '/' + f)

    @property
    def splitext(self):
        return [os.path.splitext(f) for f in self.files_except_xml]

    @property
    def png_items(self):
        return [name+ext for name, ext in self.splitext if ext in ['.png']]

    @property
    def jpg_items(self):
        return [name+ext for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]

    @property
    def tiff_items(self):
        return [name+ext for name, ext in self.splitext if ext in ['.tif', '.tiff']]

    @property
    def png_names(self):
        return [name for name, ext in self.splitext if ext in ['.png']]

    @property
    def jpg_names(self):
        return [name for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]

    @property
    def tiff_names(self):
        return [name for name, ext in self.splitext if ext in ['.tif', '.tiff']]

    def convert_images(self):
        for item in self.tiff_names:
            if item not in self.jpg_names and item not in self.png_names:
                source_fname = item + '.tif'
                if source_fname not in self.files_except_xml:
                    source_fname = item + '.tiff'
                img_utils.hdimg_to_jpg(self.path + '/' + source_fname, self.path + '/' + item + '.jpg')

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        filename = dest_path + '/' + self.name + '.zip'
        fs_utils.zip(filename, [self.path + '/' + f for f in self.all])
        return filename

    def copy_files_except_xml(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            for f in self.files_except_xml:
                shutil.copyfile(self.path + '/' + f, dest_path + '/' + f)

    def copy_xml(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            shutil.copyfile(self.filename, dest_path + '/' + self.basename)


class PackageFolder(object):

    def __init__(self, path, pkgfiles_items=None):
        self.path = path
        self.name = os.path.basename(path)
        if pkgfiles_items is None:
            self.pkgfiles_items = {}
            for item in os.listdir(path):
                if item.endswith('.xml'):
                    article_files = PkgArticleFiles(path+'/'+item)
                    self.pkgfiles_items[article_files.name] = article_files
        else:
            self.pkgfiles_items = {item.name: item for item in pkgfiles_items}
        self.INFORM_ORPHANS = len(self.pkgfiles_items) > 1

    @property
    def xml_list(self):
        return [item.filename for item in self.pkgfiles_items.values()]

    @property
    def package_filenames(self):
        items = []
        for pkg in self.pkgfiles_items.values():
            items.extend(pkg.all)
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
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        _name = os.path.basename(self.path)
        filename = dest_path + '/' + _name + '.zip'
        fs_utils.zip(filename, [self.path + '/' + f for f in self.package_filenames])
        return filename


class OutputFiles(object):

    def __init__(self, xml_name, report_path, wrk_path):
        self.xml_name = xml_name
        self.report_path = report_path
        self.wrk_path = wrk_path

        #self.related_files = []
        #self.xml_filename = xml_filename
        #self.new_xml_filename = self.xml_filename
        #self.xml_path = os.path.dirname(xml_filename)
        #self.xml_name = basename.replace('.xml', '')
        #self.new_name = self.xml_name

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
        if self.wrk_path is not None:
            if not os.path.isdir(self.wrk_path):
                os.path.makedirs(self.wrk_path)
            return self.wrk_path + '/' + self.xml_name + '.ctrl.txt'

    @property
    def style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.rep.html'

    @property
    def dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.dtd.txt'

    @property
    def pmc_dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.dtd.txt'

    @property
    def pmc_style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.rep.html'

    @property
    def err_filename(self):
        return self.report_path + '/' + self.xml_name + '.err.txt'

    @property
    def err_filename_html(self):
        return self.report_path + '/' + self.xml_name + '.err.html'

    @property
    def mkp2xml_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.mkp2xml.txt'

    @property
    def mkp2xml_report_filename_html(self):
        return self.report_path + '/' + self.xml_name + '.mkp2xml.html'

    @property
    def data_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.contents.html'

    @property
    def images_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.images.html'

    @property
    def xml_structure_validations_filename(self):
        return self.report_path + '/xmlstr-' + self.xml_name

    @property
    def xml_content_validations_filename(self):
        return self.report_path + '/xmlcon-' + self.xml_name

    @property
    def journal_validations_filename(self):
        return self.report_path + '/journal-' + self.xml_name

    @property
    def issue_validations_filename(self):
        return self.report_path + '/issue-' + self.xml_name

    def clean(self):
        for f in [self.err_filename, self.dtd_report_filename, self.style_report_filename, self.pmc_dtd_report_filename, self.pmc_style_report_filename, self.ctrl_filename]:
            fs_utils.delete_file_or_folder(f)


class AssetsDestinations(object):

    def __init__(self, pkg_path, acron, issue_label, serial_path=None, web_app_path=None, web_url=None):
        self.web_app_path = web_app_path
        self.pkg_path = pkg_path
        self.issue_path = acron + '/' + issue_label
        self.serial_path = serial_path
        self.web_url = web_url

    @property
    def result_path(self):
        if self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path
        else:
            return os.path.dirname(self.pkg_path)

    @property
    def img_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/htdocs/img/revistas/' + self.issue_path
        else:
            return self.pkg_path

    @property
    def pdf_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/bases/pdf/' + self.issue_path
        else:
            return self.pkg_path

    @property
    def xml_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/bases/xml/' + self.issue_path
        elif self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path + '/base_xml/base_source'
        else:
            return self.pkg_path

    @property
    def report_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/htdocs/reports/' + self.issue_path
        else:
            return self.result_path + '/errors'

    @property
    def report_link(self):
        if self.web_url is not None:
            return self.web_url + '/reports/' + self.issue_path
        else:
            return self.result_path + '/errors'

    @property
    def base_report_path(self):
        if self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path + '/base_xml/base_reports'

    @property
    def img_link(self):
        if self.web_url is not None:
            return self.web_url + '/img/revistas/' + self.issue_path
        else:
            return 'file://' + self.img_path

    @property
    def pdf_link(self):
        if self.web_url is not None:
            return self.web_url + '/pdf/' + self.issue_path + '/'
        else:
            return 'file://' + self.pdf_path + '/'

    @property
    def xml_link(self):
        if self.web_url is not None:
            return self.web_url + '/xml/' + self.issue_path + '/'
        else:
            return 'file://' + self.xml_path + '/'
