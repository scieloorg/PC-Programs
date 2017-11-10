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
        self.article_xml = ArticleXML(filename)
        self.article_files = workarea.PkgArticleFiles(filename)

    @property
    def files(self):
        return self.article_files.files

    @property
    def related_files(self):
        return self.article_files.related_files

    @property
    def related_files_by_name(self):
        return self.article_files.related_files_by_name

    @property
    def related_files_by_extension(self):
        return self.article_files.related_files_by_extension

    @property
    def png_items(self):
        return self.article_files.png_items

    @property
    def jpg_items(self):
        return self.article_files.jpg_items

    @property
    def tiff_items(self):
        return self.article_files.tiff_items

    @property
    def png_names(self):
        return self.article_files.png_names

    @property
    def jpg_names(self):
        return self.article_files.jpg_names

    @property
    def tiff_names(self):
        return self.article_files.tiff_names

    def svg2tiff(self):
        self.article_files.svg2tiff()

    def evaluate_tiff_images(self):
        self.article_files.evaluate_tiff_images()

    def zip(self, dest_path=None):
        return self.article_files.zip(dest_path)

    def copy_related_files(self, dest_path):
        self.article_files.copy_related_files(dest_path)

    def copy_xml(self, dest_path):
        self.article_files.copy_xml(dest_path)

    def clean(self):
        self.article_files.clean()

    def tiff2jpg(self):
        self.article_files.tiff2jpg()

    def delete_files(self, files):
        self.article_files.delete_files(files)

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
