# coding=utf-8
import os
import shutil

from ...generics import fs_utils
from ...generics import img_utils
from ...generics import xml_utils
from . import article
from . import workarea


class ArticleXML(object):

    def __init__(self, filename):
        self.filename = filename
        self.content = None
        self.xml = None
        self.xml_error = None
        self.doc = None
        self.setUp()

    def read_file(self):
        self.content = fs_utils.read_file(self.filename)

    def normalize_content(self):
        self.xml_content_handler = xml_utils.XMLContent(self.content)
        self.xml_content_handler.normalize()
        self.content = self.xml_content_handler.content

    def load_xml(self):
        self.xml, self.xml_error = xml_utils.load_xml(self.content)

    def get_article(self):
        if self.xml is not None:
            self.doc = article.Article(self.xml, os.path.basename(self.filename))

    def setUp(self):
        if os.path.isfile(self.filename):
            self.read_file()
            self.normalize_content()
            self.load_xml()
            self.get_article()


class ArticlePkg(object):

    def __init__(self, filename):
        self._prefixes = None
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
            if self.folder.endswith('_package'):
                self._prefixes = [self.name + '-', self.name + '.', ]
            else:
                if self.basename.startswith('a') and self.basename[3:4] == 'v':
                    r.append(self.basename[:3])
                r.extend([self.name + suffix for suffix in workarea.SUFFIXES])
                self._prefixes = list(set(r))
        return self._prefixes

    def find_files(self):
        r = []
        files = [item for item in self.listdir if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
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

    def update_files(self):
        if self.is_listdir_changed():
            self.files = self.find_files()
            self.update_related_files()

    def update_related_files(self):
        self.related_files = [f for f in self.files if f != self.basename and not f.endswith('.ctrl.txt')]
        self.related_files_by_name = {}
        self.related_files_by_extension = {}
        for f in self.related_files:
            name, extension = os.path.splitext(f)
            if name not in self.related_files_by_name.keys():
                self.related_files_by_name[name] = []
            if extension not in self.related_files_by_extension.keys():
                self.related_files_by_extension[extension] = []
            self.related_files_by_name[name].append(extension)
            self.related_files_by_extension[extension].append(name)

    def files_by_ext(self, extensions):
        r = []
        for ext in extensions:
            r.extend([name+ext for name in self.related_files_by_extension.get(ext, [])])
        return r

    def get_pdf_files(self):
        expected_pdf_files = self.article_xml.doc.expected_pdf_files.values()
        return [f for f in expected_pdf_files if f in self.related_files]

    def get_package_href_files(self):
        files = []
        for href_name in self.get_package_href_names():
            extensions = self.related_files_by_name.get(href_name, [])
            names = [href_name+ext for ext in extensions]
            files.extend(names)
        return files

    def get_package_href_names(self):
        href_names = []
        for href in self.article_xml.doc.href_files:
            if href.name_without_extension in self.related_files_by_name.keys():
                href_names.append(href.name_without_extension)
        return href_names

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
            fs_utils.delete_file_or_folder(self.path + '/' + f)

    def tiff2jpg(self):
        for item in self.tiff_names:
            if item not in self.jpg_names and item not in self.png_names:
                source_fname = item + '.tif'
                if source_fname not in self.related_files:
                    source_fname = item + '.tiff'
                img_utils.hdimg_to_jpg(self.path + '/' + source_fname, self.path + '/' + item + '.jpg')
        self.update_files()

    def delete_files(self, files):
        for f in files:
            fs_utils.delete_file_or_folder(self.path + '/' + f)
        self.update_files()

    def select_pmc_files(self):
        files = []
        for item in self.get_package_href_names():
            if item in self.tiff_names:
                if item+'.tif' in self.tiff_items:
                    files.append(item+'.tif')
                elif item+'.tiff' in self.tiff_items:
                    files.append(item+'.tiff')
            else:
                files.extend(self.related_files_by_name.get(item, []))
        files.extend(self.get_pdf_files())
        return files

    def svg2tiff(self):
        sgv_items = self.files_by_ext(['.svg'])
        if len(self.tiff_items) == 0 and len(sgv_items) > 0:
            for item in sgv_items:
                img_utils.convert_svg2png(self.path + '/' + item)
            self.update_files()
            for item in self.files_by_ext(['.png']):
                img_utils.convert_png2tiff(self.path + '/' + item)
            self.update_files()

    def evaluate_tiff_images(self):
        errors = []
        for f in self.tiff_items:
            errors.append(img_utils.validate_tiff_image_file(self.path+'/'+f))
        return [e for e in errors if e is not None]

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        filename = dest_path + '/' + self.name + '.zip'
        fs_utils.zip(filename, [self.path + '/' + f for f in self.files])
        return filename

    def copy_related_files(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            for f in self.related_files:
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
