# coding=utf-8

import os

from ..useful import fs_utils
from ..data import article
from . import workarea


class Package(object):

    def __init__(self, input_xml_list, workarea_path):
        self.input_xml_list = input_xml_list
        self.input_path = os.path.dirname(input_xml_list[0])
        self.wk = workarea.Workarea(workarea_path)
        self.pkgissuedata = PackageIssueData(self.articles)

    @property
    def package_folder(self):
        return workarea.PackageFolder(self.wk.scielo_package_path, self.input_xml_list)

    @property
    def articles_xml_content(self):
        return {item.name: article.ArticleXMLContent(fs_utils.read_file(item.filename), item.previous_name, item.name) for item in self.package_folder.pkgfiles_items.values()}

    @property
    def articles(self):
        return {name: item.doc for name, item in self.articles_xml_content.items()}

    @property
    def outputs(self):
        return {item.name: workarea.OutputFiles(item.previous_name, self.wk.reports_path, item.ctrl_path) for item in self.package_folder.pkgfiles_items.values()}

    @property
    def is_pmc_journal(self):
        return any([doc.journal_id_nlm_ta is not None for name, doc in self.articles.items()])


class PackageIssueData(object):

    def __init__(self, articles):
        self.articles = articles
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None
        self.journal = None
        self.journal_data = None
        self._issue_label = None

    def setup(self):
        data = list(set([(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in self.articles.values()]))
        data.sort(reverse=True)
        if len(data) > 0:
            data = list(data[0])
            if any(data):
                self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label = data

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
