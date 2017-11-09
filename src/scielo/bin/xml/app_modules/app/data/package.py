# coding=utf-8
import os
import shutil

from ...generics import fs_utils
from ...generics import xml_utils
from . import article
from . import workarea


class ArticleXML(object):

    def __init__(self, filename):
        self.content = fs_utils.read_file(filename)
        self.xml_content = xml_utils.XMLContent(self.content)

    def normalize_content(self):
        self.xml_content.normalize()
        self.content = self.xml_content.content

    def load_xml(self):
        self.xml, self.xml_error = xml_utils.load_xml(self.content)

    def get_doc(self):
        self.normalize_content()
        self.load_xml()
        if self.xml is not None:
            return article.Article(self.xml, self.file.basename)

    @property
    def doc(self):
        if not hasattr('_doc'):
            self._doc = self.get_doc()
        return self._doc


class ArticlePkg(object):

    def __init__(self, filename):
        self.article_xml = ArticleXML(filename)
        self.filename = filename
        self.path = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)

        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        self.folder = os.path.basename(self.path)
        if self.filename.endswith('.sgm.xml'):
            self.name, ign = os.path.splitext(self.name)
        self.previous_name = self.name
        self.listdir = []
        self.update_files()

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

    def find_files(self):
        r = []
        files = [item for item in self.listdir if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
        for item in files:
            selected = [item for prefix in self.prefixes if item.startswith(prefix)]
            r.extend(selected)
        return list(set(r))

    def update_listdir(self):
        listdir = os.listdir(self.path)
        if set(listdir) != set(self.listdir):
            self.listdir = listdir
            return True
        return False

    def update_files(self):
        if self.update_listdir():
            self.files = self.find_files()
            self.update_files_except_xml()
            self.update_files_by_name_except_xml()
            self.splitext = [os.path.splitext(f) for f in self.files_except_xml]
            self.png_items = [name+ext for name, ext in self.splitext if ext in ['.png']]
            self.jpg_items = [name+ext for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]
            self.tiff_items = [name+ext for name, ext in self.splitext if ext in ['.tif', '.tiff']]
            self.png_names = [name for name, ext in self.splitext if ext in ['.png']]
            self.jpg_names = [name for name, ext in self.splitext if ext in ['.jpg', '.jpeg']]
            self.tiff_names = [name for name, ext in self.splitext if ext in ['.tif', '.tiff']]

    def update_files_except_xml(self):
        self.files_except_xml = [f for f in self.files if f != self.basename and not f.endswith('.ctrl.txt')]

    def update_files_by_name_except_xml(self):
        files = {}
        for f in self.files_except_xml:
            name, ext = os.path.splitext(f)
            if name not in files.keys():
                files[name] = []
            files[name].append(ext)
        self.files_by_name_except_xml = files

    def clean(self):
        for f in self.files_except_xml:
            fs_utils.delete_file_or_folder(self.path + '/' + f)

    def tiff2jpg(self):
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
        fs_utils.zip(filename, [self.path + '/' + f for f in self.files])
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


class Package(object):

    def __init__(self, pkgfiles_items, outputs, workarea_path):
        self.pkgfiles_items = pkgfiles_items
        self.package_folder = workarea.PackageFolder(pkgfiles_items[0].path, pkgfiles_items)
        self.outputs = outputs
        self.wk = workarea.Workarea(workarea_path)
        self._articles = None
        self._articles_xml_content = None
        self.issue_data = PackageIssueData()
        self.issue_data.setup(self.articles)

    @property
    def articles_xml_content(self):
        if self._articles_xml_content is None:
            self._articles_xml_content = {item.name: article.ArticleXMLContent(fs_utils.read_file(item.filename), item.previous_name, item.name) for item in self.pkgfiles_items}
        return self._articles_xml_content

    @property
    def articles(self):
        if self._articles is None:
            self._articles = {name: item.doc for name, item in self.articles_xml_content.items()}
        return self._articles

    @property
    def is_pmc_journal(self):
        return any([doc.journal_id_nlm_ta is not None for name, doc in self.articles.items()])


class PackageIssueData(object):

    def __init__(self):
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None
        self.journal = None
        self.journal_data = None
        self._issue_label = None

    def setup(self, articles):
        data = [(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in articles.values() if a.tree is not None]
        if len(data) > 0:
            self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label = self.select(data)

    def select(self, data):
        _data = []
        for item in list(set(data)):
            _data.append([field if field is not None else '' for field in item])
        _data = sorted(_data, reverse=True)
        return [item if item != '' else None for item in _data[0]]

    @property
    def acron(self):
        a = 'unknown_acron'
        if self.journal is not None:
            if self.journal.acron is not None:
                a = self.journal.acron
        return a

    @property
    def acron_issue_label(self):
        return self.acron + ' ' + self.issue_label

    @property
    def issue_label(self):
        r = self._issue_label if self._issue_label else self.pkg_issue_label
        if r is None:
            r = 'unknown_issue_label'
        return r
