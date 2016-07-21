import os

import xpchecker


class ArticlesData(object):

    def __init__(self, pkg_articles, journals, issues, previous_registered_articles, is_db_generation):
        pass


class ArticlesSetValidations(object):

    def __init__(self, pkg_articles, journals, issues, previous_registered_articles):
        self.pkg_articles = pkg_articles

    def validate(self, dtd_files):
        self.validations = {}
        for name, article in self.pkg_articles.articles.items():
            article_validations = ArticleValidations(article, doc_files_info_items[name], dtd_files)
            self.validations[name] = [
                article_validations.xml_structure_validations,
                article_validations.xml_content_validations,
            ]


class ArticleValidations(object):

    def __init__(self, article, doc_files_info, dtd_files):
        self.article = article
        self.doc_files_info = doc_files_info
        self.dtd_files = dtd_files

    @property
    def xml_structure_validations(self):
        new_name = self.doc_files_info.new_name

        for f in [self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename, self.doc_files_info.data_report_filename, self.doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        xml_filename = self.doc_files_info.new_xml_filename

        xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, self.dtd_files, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename)
        xml_f, xml_e, xml_w = valid_style

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            separator = ''
            if os.path.isfile(self.doc_files_info.err_filename):
                separator = '\n\n\n' + '.........\n\n\n'
            open(self.doc_files_info.err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(self.doc_files_info.dtd_report_filename, 'r').read())

        if xml is None:
            xml_f += 1
        if not valid_dtd:
            xml_f += 1
        if self.doc_files_info.ctrl_filename is None:
            if xml_f + xml_e + xml_w == 0:
                os.unlink(self.doc_files_info.style_report_filename)
        else:
            open(self.doc_files_info.ctrl_filename, 'w').write('Finished')

        if os.path.isfile(self.doc_files_info.dtd_report_filename):
            os.unlink(self.doc_files_info.dtd_report_filename)

        report_content = ''
        for rep_file in [self.doc_files_info.err_filename, self.doc_files_info.dtd_report_filename, self.doc_files_info.style_report_filename]:
            if os.path.isfile(rep_file):
                report_content += extract_report_core(fs_utils.read_file(rep_file))
                #if is_xml_generation is False:
                #    fs_utils.delete_file_or_folder(rep_file)
        return ValidationsResults(report_content)


class PkgReports(object):

    def __init__(self, articles_set_validations):
        self.articles_set_validations = articles_set_validations


