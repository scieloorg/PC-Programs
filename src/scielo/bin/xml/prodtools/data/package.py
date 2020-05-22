# coding=utf-8
import logging
import logging.config

from prodtools.utils import xml_utils
from prodtools.data import article
from prodtools.data import workarea


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class SPPackage(object):
    """
    Contém dados (files + xml + article) de um conjunto de documentos
    de um mesmo número
    """

    def __init__(self, path, output_path, xml_names, sgmxml_name=None,
                 optimised=False):
        self.package_folder = workarea.MultiDocsPackageFolder(path)
        self.wk = workarea.MultiDocsPackageOuputs(output_path)
        self.xml_names = xml_names
        self.optimised = optimised
        self._articles = {}
        if xml_names:
            for name, item in self.files.items():
                if item.basename not in xml_names:
                    continue
                xml, xml_error = xml_utils.load_xml(item.filename)
                self._articles[name] = article.Article(xml, name)
                self.wk.get_doc_outputs(name, sgmxml_name)
        self.issue_data = PackageIssueData()
        self.issue_data.setup(self._articles)
        if len(xml_names) < len(self.package_folder.pkgfiles_items):
            print("SPPackage have {} documents. "
                  "{} was filtered to be processed.".format(
                    len(self.package_folder.pkgfiles_items), len(xml_names)
                  ))

    @property
    def file_paths(self):
        return self.package_folder.file_paths

    @property
    def files(self):
        return self.package_folder.pkgfiles_items

    @property
    def articles(self):
        logger.info("package.articles: %s" % len(self._articles))
        return self._articles

    @property
    def outputs(self):
        return self.wk.doc_outs

    @property
    def is_pmc_journal(self):
        for doc in self.articles.values():
            if doc.journal_id_nlm_ta:
                return True

    def zip(self):
        if not self.optimised:
            self.package_folder.zip()
        for name, pkgfiles in self.package_folder.pkgfiles_items.items():
            pkgfiles.zip(self.package_folder.path + '_zips')


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
