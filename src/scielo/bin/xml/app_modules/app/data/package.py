# coding=utf-8

from ...generics import fs_utils
from . import article
from . import workarea


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
            print(self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label)

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
