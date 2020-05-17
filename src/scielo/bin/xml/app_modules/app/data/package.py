# coding=utf-8
from ...generics import xml_utils
from . import article
from . import workarea


class PMC_DocumentPackage(workarea.DocumentPackageFiles):

    def __init__(self, filename):
        super().__init__(self, filename)
        self.xml_content = xml_utils.SuitableXML(filename)
        self.article_xml = self.xml_content.content

    @property
    def article_xml(self):
        return self._article_xml

    @article_xml.setter
    def article_xml(self, content):
        self.xml_content.content = content
        self._article_xml = article.Article(self.xml_content.xml, self.basename)

    def get_pdf_files(self):
        expected_pdf_files = self.article_xml.expected_pdf_files.values()
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
        for href in self.article_xml.href_files:
            if href.name_without_extension in self.related_files_by_name.keys():
                href_names.append(href.name_without_extension)
        return list(set(href_names))

    def select_pmc_files(self):
        files = []
        for item in self.get_package_href_names():
            if item in self.tiff_names:
                if item+'.tif' in self.tiff_items:
                    files.append(item+'.tif')
                elif item+'.tiff' in self.tiff_items:
                    files.append(item+'.tiff')
            else:
                files.extend([item + ext for ext in self.related_files_by_name.get(item, [])])
        files.extend(self.get_pdf_files())
        return files


class SPPackage(object):
    """
    Contém dados (files + xml + article) de um conjunto de documentos
    de um mesmo número
    """

    def __init__(self, path, output_path, xml_list):
        self.package_folder = workarea.MultiDocsPackageFolder(path)
        self.wk = workarea.MultiDocsPackageOuputs(output_path)
        self.xml_list = xml_list
        self._articles = {}
        if xml_list:
            for name, item in self.files.items():
                if item.filename not in xml_list:
                    continue
                xml, xml_error = xml_utils.load_xml(item.filename)
                self._articles[name] = article.Article(xml, name)
                self.wk.get_doc_outputs(name)

        self.issue_data = PackageIssueData()
        self.issue_data.setup(self._articles)

    @property
    def file_paths(self):
        return self.package_folder.file_paths

    @property
    def files(self):
        return self.package_folder.pkgfiles_items

    @property
    def articles(self):
        return self._articles

    @property
    def outputs(self):
        print(self.wk.doc_outs)
        return self.wk.doc_outs

    @property
    def is_pmc_journal(self):
        print(self._articles)
        for doc in self.articles.values():
            if doc.journal_id_nlm_ta:
                return True


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
