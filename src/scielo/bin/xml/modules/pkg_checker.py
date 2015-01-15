# coding=utf-8

import os

import xml_utils
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


def article_validations_reports_content(filename):
    content = ''
    if os.path.isfile(filename):
        content = open(filename, 'r').read()
        if '</article>' in content:
            content = html_report.display_xml(content)
            content = content.replace('\n', '<br/>')

        if '</body>' in content:
            content = content[content.find('<body'):]
            content = content[0:content.rfind('</body>')]
            content = content[content.find('>')+1:]
    return content


def sum_stats(stats_items):
    f = sum([i[0] for i in stats_items])
    e = sum([i[1] for i in stats_items])
    w = sum([i[2] for i in stats_items])
    return (f, e, w)


def articles_stats_report(articles_stats_and_reports):
    xml_f, xml_e, xml_w = sum_stats([item[0] for item in articles_stats_and_reports.values()])
    data_f, data_e, data_w = sum_stats([item[1] for item in articles_stats_and_reports.values()])
    return stats_report(xml_f, xml_e, xml_w, 'articles xml validations') + stats_report(data_f, data_e, data_w, 'articles data validations')


def stats_report(f, e, w, title):
    return html_report.statistics_messages(f, e, w, title)


def xml_list(pkg_path, xml_filenames):
    r = ''
    r += '<h2>XML files</h2>'
    r += 'XML path: ' + pkg_path
    r += 'Total of XML files: ' + str(len(xml_filenames))
    r += html_report.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames])
    return r


def incr(d, value):
    if value is not None:
        if not value in d.keys():
            d[value] = 0
        d[value] += 1
    return d


def more_frequent(d):
    r = None
    t = 0
    for k, v in d.items():
        if v > t:
            t = v
            r = k
    return r


def articles_and_issues(doc_files_info_list):
    articles = {}
    issue_labels = {}
    e_issns = {}
    p_issns = {}

    for doc_files_info in doc_files_info_list:
        new_name = doc_files_info.new_name
        xml_filename = doc_files_info.new_xml_filename
        xml, e = xml_utils.load_xml(xml_filename)

        articles[new_name] = Article(xml) if xml is not None else None
        if xml is not None:
            issue_labels = incr(issue_labels, articles[new_name].issue_label)
            p_issns = incr(p_issns, articles[new_name].print_issn)
            e_issns = incr(e_issns, articles[new_name].e_issn)

    issue_label = more_frequent(issue_labels)
    p_issn = more_frequent(p_issns)
    e_issn = more_frequent(e_issns)
    return (articles, (issue_label, p_issn, e_issn))


def package_validations_data(articles, doc_files_info_list, dtd_files, report_path, validate_order, create_toc_report):
    articles_stats_and_reports = {}
    lists = ''
    toc_f, toc_e, toc_w = (0, 0, 0)
    toc_authors_sheet_data = []
    toc_sources_sheet_data = []
    authors_h = None
    authors_w = None
    sources_h = None
    sources_w = None
    toc_stats_and_report = ((toc_f, toc_e, toc_w), '')

    if create_toc_report:
        toc_f, toc_e, toc_w, toc_report = article_checker.toc_report(articles, validate_order)
        toc_stats_and_report = ((toc_f, toc_e, toc_w), toc_report)

    if toc_f == 0:
        index = 0
        for doc_files_info in doc_files_info_list:
            new_name = doc_files_info.new_name
            xml_filename = doc_files_info.new_xml_filename

            index += 1
            print(new_name)

            xml_f, xml_e, xml_w = validate_article_xml(new_name, xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)

            data_f, data_e, data_w, sheet_data = validate_article_data(articles[new_name], new_name, os.path.dirname(xml_filename), doc_files_info.data_report_filename, validate_order)

            #html += html_report.collapsible_block(os.path.basename(xml_filename), reports.body(xml_filename.replace()))
            xml_report = article_validations_reports_content(doc_files_info.dtd_report_filename) + article_validations_reports_content(doc_files_info.style_report_filename)
            data_report = article_validations_reports_content(doc_files_info.data_report_filename)
            articles_stats_and_reports[new_name] = ((xml_f, xml_e, xml_w, xml_report), (data_f, data_e, data_w, data_report))

            if create_toc_report and sheet_data is not None:
                authors_h, authors_w, authors_data = sheet_data.authors_sheet_data(new_name)
                toc_authors_sheet_data += authors_data
                sources_h, sources_w, sources_data = sheet_data.sources_sheet_data(new_name)
                toc_sources_sheet_data += sources_data

    if create_toc_report:
        authors = html_report.sheet((authors_h, authors_w, toc_authors_sheet_data))
        authors = html_report.collapsible_block('authors', 'List of authors found in the package', authors)

        sources = html_report.sheet((sources_h, sources_w, toc_sources_sheet_data))
        sources = html_report.collapsible_block('sources', 'List of sources found in the package', sources)

        lists = authors + sources

    return (toc_stats_and_report, articles_stats_and_reports, lists)


def display_statistics_inline(f, e, w):
    return ' | '.join([k + ': ' + v for k, v in {'fatal errors': str(f), 'errors': str(e), 'warnings': str(w)}.items()])


def package_validation_report_content(toc_stats_and_report, articles_stats_and_reports, lists):
    text = ''
    toc_f = 0
    if toc_stats_and_report is not None:
        toc_stats, toc_report = toc_stats_and_report
        toc_f, toc_e, toc_w = toc_stats

        if toc_f + toc_e + toc_w > 0:
            text += html_report.tag('h3', 'Table of Contents Report')
            text += stats_report(toc_f, toc_e, toc_w, 'toc validations stats')
            text += html_report.collapsible_block('table of contents', 'table of contents', toc_report)

    text += lists

    if toc_f == 0:
        n = '/' + str(len(articles_stats_and_reports))
        index = 0
        text += html_report.tag('h3', 'XML and Data Validations Report')

        for name, items in articles_stats_and_reports.items():
            i = 0
            index += 1

            text += html_report.tag('h4', str(index) + n)
            text += html_report.tag('h4', name + '.xml')

            items = {'xml validation': items[0], 'data validation': items[1]}
            for report_name, item in items.items():
                f, e, w, report = item
                i += 1
                title = name + '.xml ' + report_name + ' [' + display_statistics_inline(f, e, w) + ']'
                if f + e + w > 0:
                    text += html_report.collapsible_block(name + str(i), title, report)
    return text


def processing_result_location(result_path):
    return 'Result of the processing: ' + html_report.link('file:///' + os.path.dirname(result_path), os.path.dirname(result_path))


def save_report(filename, title, content):
    html_report.title = title
    html_report.body = content
    html_report.save(filename)
    print('\n\nReport:\n ' + filename)


def display_report(report_filename):
    try:
        os.system('python -mwebbrowser file:///' + report_filename.replace('//', '/'))
    except:
        pass
