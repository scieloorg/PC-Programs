# coding=utf-8

import os
import shutil

from . import fs_utils
from . import img_utils


class Workarea(object):

    def __init__(self, filename, output_path=None):
        self.input_pkgfiles = PackageFiles(filename)
        self.xml_pkgfiles = None
        if not filename.endswith('.sgm.xml'):
            self.xml_pkgfiles = self.input_pkgfiles
        self.output_path = output_path or os.path.dirname(self.input_pkgfiles.path)
        self.outputs = OutputFiles(self.input_pkgfiles.name, self.reports_path, self.input_pkgfiles.path)
        self._scielo_pkg_files = None
        self._pmc_pkgfiles = None
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

    @property
    def scielo_pkgfiles(self):
        if self._scielo_pkg_files is None:
            if self.xml_pkgfiles is not None:
                self._scielo_pkg_files = PackageFiles(self.scielo_package_path + '/' + self.xml_pkgfiles.basename)
        return self._scielo_pkg_files

    @property
    def pmc_pkgfiles(self):
        if self._pmc_pkg_files is None:
            if self.xml_pkgfiles is not None:
                self._pmc_pkg_files = PackageFiles(self.pmc_package_path + '/' + self.xml_pkgfiles.basename)
        return self._pmc_pkg_files


class PackageFiles(object):

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)

    @property
    def extensions(self):
        return list(set([f[f.rfind('.'):] for f in os.listdir(self.path) if f.startswith(self.name + '.')]))

    def name_with_extension(self, href, new_href):
        if '.' not in new_href:
            extensions = self.extensions
            if len(extensions) > 1:
                extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
            if len(extensions) > 0:
                new_href += extensions[0]
        return new_href

    @property
    def files(self):
        r = [item for item in os.listdir(self.path) if (item.startswith(self.name + '-') or item.startswith(self.name + '.')) and not item.endswith('.xml')]
        suffixes = ['t', 'f', 'e', 'img', 'image']
        suffixes.extend(['-'+s for s in suffixes])
        for suffix in suffixes:
            r += [item for item in os.listdir(self.path) if item.startswith(self.name + suffix)]
        r = list(set(r))
        r = [item for item in r if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
        return sorted(r)

    @property
    def files_by_name(self):
        files = {}
        for f in self.files:
            name, ext = os.path.splitext(f)
            if name not in files.keys():
                files[name] = []
            files[name].append(ext)
        return files

    def clean(self):
        for f in self.files:
            fs_utils.delete_file_or_folder(self.path + '/' + f)

    @property
    def splitext(self):
        return [os.path.splitext(f) for f in self.files]

    @property
    def png_files(self):
        return [name for name, ext in self.splitext if ext in ['.png']]

    @property
    def jpg_files(self):
        return [name for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]

    @property
    def tif_files(self):
        return [name for name, ext in self.splitext if ext in ['.tif', '.tiff']]

    def convert_images(self):
        for item in self.tif_files:
            if not item in self.jpg_files and not item in self.png_files:
                source_fname = item + '.tif'
                if not source_fname in self.files:
                    source_fname = item + '.tiff'
                img_utils.hdimg_to_jpg(self.path + '/' + source_fname, self.path + '/' + item + '.jpg')
                if os.path.isfile(self.path + '/' + item + '.jpg'):
                    self.files.append(item + '.jpg')

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        filename = dest_path + '/' + self.name + '.zip'
        fs_utils.zip(filename, [self.path + '/' + f for f in self.files])
        return filename

    def copy(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            for f in self.files:
                shutil.copyfile(self.path + '/' + f, dest_path + '/' + f)


class PackageFolder(object):

    def __init__(self, path):
        self.path = path
        self.xml_list = [self.path + '/' + f for f in os.listdir(self.path) if f.endswith('.xml') and not f.endswith('.sgm.xml')]

    @property
    def packages(self):
        items = []
        for item in self.xml_list:
            items.append(PackageFiles(item))
        return items

    @property
    def package_files(self):
        items = []
        for pkg in self.packages:
            items.extend(pkg.files)
        return items

    @property
    def orphans(self):
        items = []
        for f in os.listdir(self.path):
            if f not in self.package_files:
                items.append(f)
        return items

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        filename = dest_path + '/' + os.path.basename(self.path) + '.zip'
        fs_utils.zip(filename, [self.path + '/' + f for f in self.package_files])
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

