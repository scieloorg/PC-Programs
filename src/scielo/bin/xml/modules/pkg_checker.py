# coding=utf-8
import os

import files_manager
import article_checker
import xpchecker
import reports

from article import Article


html_report = reports.ReportHTML()


def validate_article_xml(new_name, xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename):
    xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename)
    f, e, w = valid_style
    if xml is None:
        f += 1
    if not valid_dtd:
        w += 1
    return (f, e, w)


def validate_article_data(article, new_name, package_path, report_filename, validate_order):
    f, e, w, sheet_data = article_checker.validate_article_data(article, new_name, package_path, report_filename, validate_order)
    return (f, e, w, sheet_data)


def validate_article(xml_filename, new_name, report_name, doc_files_info, dtd_files, validate_order):
    xml = article_checker.get_valid_xml(xml_filename)

    xml_f, xml_e, xml_w = validate_article_xml(new_name, xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)

    if xml is None:
        article = None
    else:
        article = Article(xml)

    data_f, data_e, data_w, sheet_data = validate_article_data(article, new_name, os.path.dirname(xml_filename), doc_files_info.data_report_filename, validate_order)

    result = html_report.tag('h3', report_name)

    result += html_report.tag('p', html_report.link('file:///' + xml_filename, os.path.basename(xml_filename)))
    result += html_report.statistics_messages(xml_f, xml_e, xml_w, 'xml validations', [doc_files_info.err_filename, doc_files_info.style_report_filename])

    result += html_report.statistics_messages(data_f, data_e, data_w, 'data validations', [doc_files_info.data_report_filename])
    return (article, sheet_data, result, (xml_f, xml_e, xml_w), (data_f, data_e, data_w))


def validate_package(doc_files_info_list, dtd_files, report_path, validate_order, create_toc_report):

    toc_authors_sheet_data = []
    toc_sources_sheet_data = []
    authors_h = None
    authors_w = None
    sources_h = None
    sources_w = None
    issues = []

    articles = {}
    article_results = {}

    xml_f, xml_e, xml_w = (0, 0, 0)
    data_f, data_e, data_w = (0, 0, 0)

    for doc_files_info in doc_files_info_list:
        new_name = doc_files_info.new_name
        report_name = doc_files_info.xml_name
        xml_filename = doc_files_info.new_xml_filename
        print(new_name)
        article, sheet_data, result, xml_stats, data_stats = validate_article(xml_filename, new_name, report_name, doc_files_info, dtd_files, validate_order)

        f, e, w = xml_stats
        xml_f += f
        xml_e += e
        xml_w += w

        f, e, w = data_stats
        data_f += f
        data_e += e
        data_w += w

        article_results[new_name] = (xml_stats, data_stats, result)

        if article is not None:
            if not article.issue_label in issues:
                issues.append(article.issue_label)
            articles[new_name] = article

        if sheet_data is not None:
            authors_h, authors_w, authors_data = sheet_data.authors_sheet_data(new_name)
            sources_h, sources_w, sources_data = sheet_data.sources_sheet_data(new_name)

            if create_toc_report:
                toc_authors_sheet_data += authors_data
                toc_sources_sheet_data += sources_data

    toc_stats = ''
    toc_results = None
    articles_stats = html_report.statistics_messages(xml_f, xml_e, xml_w, 'articles xml validations') + html_report.statistics_messages(data_f, data_e, data_w, 'articles data validations')

    if create_toc_report:
        html_report.title = 'Authors'
        html_report.body = html_report.sheet((authors_h, authors_w, toc_authors_sheet_data))
        html_report.save(report_path + '/authors.html')

        html_report.title = 'Sources'
        html_report.body = html_report.sheet((sources_h, sources_w, toc_sources_sheet_data))
        html_report.save(report_path + '/sources.html')

        toc_f, toc_e, toc_w, toc_report = article_checker.toc_report(articles, validate_order)
        toc_stats = html_report.statistics_messages(toc_f, toc_e, toc_w, 'table of contents validations')
        toc_results = ((toc_f, toc_e, toc_w), toc_stats)

        html_report.save(report_path + '/toc.html', 'TOC Report', toc_stats + toc_report)

    return (issues, toc_results, articles, articles_stats, article_results)


def display_report(report_filename):
    try:
        os.system('python -mwebbrowser file:///' + report_filename.replace('//', '/'))
    except:
        pass
