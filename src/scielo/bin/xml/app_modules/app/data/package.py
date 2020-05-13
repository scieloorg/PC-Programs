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


class PackageItem(object):
    def __init__(self, pkgfiles):
        """
        artfiles
            <class 'app_modules.app.data.workarea.PkgArticleFiles'>
        """
        self.suitable_xml = xml_utils.SuitableXML(
            pkgfiles.filename, do_changes=False)
        self.article = article.Article(self.suitable_xml.xml, pkgfiles.name)
        self.files = pkgfiles


class MultiDocsPackage(object):
    """
    Contém dados (files + xml + article) de um conjunto de documentos
    de um mesmo número
    """

    def __init__(self, pkgfiles_items, outputs, workarea_path):
        """
        pkgfiles_items
            list of <class 'app_modules.app.data.workarea.PkgArticleFiles'>
        """
        self.package_folder = workarea.MutiDocsPackageFolder(
            pkgfiles_items[0].path, pkgfiles_items)
        # self.input_zip_file_path = self.package_folder.zip()
        self.outputs = outputs
        self.wk = workarea.Workarea(workarea_path)
        self._file_paths = {item.name: item.filename
                            for item in pkgfiles_items}

        self.package_items = {}
        for item in pkgfiles_items:
            self.package_items[item.name] = PackageItem(item)

        self.issue_data = PackageIssueData()
        self.issue_data.setup(self.articles)

    @property
    def file_paths(self):
        return {name: item.filename
                for name, item in self.package_items.items()}

    @property
    def articles(self):
        return {name: pkg_item.article
                for name, pkg_item in self.package_items.items()}

    @property
    def is_pmc_journal(self):
        for doc in self.articles.values():
            if doc.journal_id_nlm_ta:
                return True


# def normalize_xml_packages(xml_list, dtd_location_type, stage):
#     article_files_items = [workarea.PkgArticleFiles(item) for item in xml_list]

#     path = article_files_items[0].path + '_' + stage

#     if not os.path.isdir(path):
#         os.makedirs(path)

#     wk = workarea.Workarea(path)
#     outputs = {}
#     dest_path = wk.scielo_package_path
#     dest_article_files_items = [workarea.PkgArticleFiles(dest_path + '/' + item.basename) for item in article_files_items]
#     for src, dest in zip(article_files_items, dest_article_files_items):
#         src.tiff2jpg()
#         xmlcontent = sps_pkgmaker.SPSXMLContent(src.filename)
#         xmlcontent.write(
#             dest.filename,
#             dtd_location_type=dtd_location_type, pretty_print=True)
#         src.copy_related_files(dest_path)

#         outputs[dest.name] = workarea.OutputFiles(dest.name, wk.reports_path, None)

#     return dest_article_files_items, outputs

# from packtools.utils import XMLWebOptimiser
# from packtools.domain import XMLValidator

#     def optimize(self):
#         def read_file(f):
#             with open(f, "rb") as fp:
#                 return fp.read()

#         xml_validator = XMLValidator(self.xml)
#         xml_web_optimiser = XMLWebOptimiser(
#             self.filename, xml_validator.assets,
#             read_file, self.pkg_path, stop_if_error=False
#         )
#         b_file_content = xml_web_optimiser.get_xml_file()
#         self.content = b_file_content.decode("utf-8")
#         for 
#         , get_optimised_assets, get_assets_thumbnail
#         xml_web_optimiser.optimise()

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
