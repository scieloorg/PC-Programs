import os

from . import fs_utils
from . import img_utils


class Workarea(object):

    def __init__(self, filename, output_path=None):
        self.package_files = PackageFiles(filename)
        self.output_path = output_path or os.path.dirname(self.package_files.path)
        self.output_files = OutputFiles(self.package_files.name, self.reports_path, self.package_files.input_path)
        self.new_package_files = None

    @property
    def reports_path(self):
        return self.output_path + '/errors'

    @property
    def scielo_package_path(self):
        return self.output_path + '/scielo_package'

    @property
    def scielo_package_filename(self):
        return self.scielo_package_path+'/'+self.new_package_files.name+'.xml'

    @property
    def temporary_package_filename(self):
        return self.input_path+'/'+self.new_package_files.name+'.xml'

    @property
    def pmc_package_path(self):
        return self.output_path+'/pmc_package'

    def copy(self):
        for f in self.package_files.files:
            shutil.copyfile(self.package_files.path + '/' + f, self.new_package_files.path + '/' + f)


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


class OutputFiles(object):

    def __init__(self, xml_name, report_path, wrk_path):
        self.xml_name = xml_name
        self.report_path = report_path
        self.wrk_path = wrk_path

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


