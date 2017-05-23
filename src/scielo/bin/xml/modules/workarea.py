import os

from . import fs_utils


class Package(object):

    def __init__(self):
        self.href_files = None


class ReportFiles(object):

    def __init__(self, xml_name, report_path, wrk_path=None):
        self.ctrl_filename = None
        self.html_filename = None
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
    def html_filename(self):
        if self.wrk_path is not None:
            return self.wrk_path + '/' + self.xml_name + '.temp.htm'

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


class Workarea(object):

    def __init__(self, filename, output_path=None):
        self.filename = filename
        self.dirname = os.path.dirname(filename)
        self.output_path = output_path or os.path.dirname(self.dirname)
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)
        self.new_name = self.name
        self.reports = ReportFiles(self.name, self.reports_path, self.dirname)

    @property
    def reports_path(self):
        return self.output_path + '/errors'

    @property
    def valid_package_path(self):
        return self.output_path + '/scielo_package'

    @property
    def valid_package_filename(self):
        return self.valid_package_path + '/' + self.new_name + '.xml'

    @property
    def generated_package_path(self):
        return self.dirname

    @property
    def generated_package_filename(self):
        return self.generated_package_path + '/' + self.new_name + '.xml'

    @property
    def pmc_package_path(self):
        return self.output_path + '/pmc_package'

    def extensions(self, filename):
        return list(set([f[f.rfind('.'):] for f in os.listdir(self.dirname) if f.startswith(filename + '.')]))

    def name_with_extension(self, href, new_href):
        if '.' not in new_href:
            extensions = self.extensions(href)
            if len(extensions) > 1:
                extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
            if len(extensions) > 0:
                new_href += extensions[0]
        return new_href

    @property
    def article_files(self):
        r = [item for item in os.listdir(self.dirname) if (item.startswith(self.name + '-') or item.startswith(self.name + '.')) and not item.endswith('.xml')]
        suffixes = ['t', 'f', 'e', 'img', 'image']
        suffixes.extend(['-'+s for s in suffixes])
        for suffix in suffixes:
            r += [item for item in os.listdir(self.dirname) if item.startswith(self.name + suffix)]
        r = list(set(r))
        r = [item for item in r if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
        return sorted(r)

    @property
    def sorted_article_files(self):
        files = {}
        for f in self.article_files:
            name, ext = os.path.splitext(f)
            if name not in files.keys():
                files[name] = []
            files[name].append(ext)
        return files
