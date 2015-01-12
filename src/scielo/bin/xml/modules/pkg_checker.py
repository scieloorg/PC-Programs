# coding=utf-8
import os
import shutil

import xml_utils
import article_checker
import xpchecker
import reports

from article import Article


html_report = reports.ReportHTML()


def get_valid_xml(xml_filename, report_path, old_name):
    xml, e = xml_utils.load_xml(xml_filename)
    if xml is None:
        if not os.path.isdir(report_path):
            os.makedirs(report_path)
        fname = os.path.basename(xml_filename)

        _xml_content = open(xml_filename, 'r').read()
        xml_content, replaced_named_ent = xml_utils.convert_entities_to_chars(_xml_content)
        if xml_content != _xml_content:
            if len(replaced_named_ent) > 0:
                open(report_path + '/' + fname + '.replaced.txt', 'w').write('\n'.join(replaced_named_ent))

            xml, e = xml_utils.load_xml(xml_content)
            if not xml is None:
                if os.path.dirname(xml_filename) != report_path:
                    shutil.copyfile(xml_filename, report_path + '/' + fname + '.bkp')
                open(xml_filename, 'w').write(xml_content)
    if xml is None:
        shutil.copyfile(xml_filename, report_path + '/' + fname.replace('.xml', '_incorrect.xml'))

    return xml


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


def old_validate_article(xml_filename, new_name, report_name, doc_files_info, dtd_files, validate_order):
    xml = get_valid_xml(xml_filename, os.path.dirname(doc_files_info.dtd_report_filename), report_name)

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


def validate_article_report_data(xml_filename, new_name, report_name, doc_files_info, dtd_files, validate_order):
    xml = get_valid_xml(xml_filename, os.path.dirname(doc_files_info.dtd_report_filename), report_name)

    xml_f, xml_e, xml_w = validate_article_xml(new_name, xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)

    if xml is None:
        article = None
    else:
        article = Article(xml)

    data_f, data_e, data_w, sheet_data = validate_article_data(article, new_name, os.path.dirname(xml_filename), doc_files_info.data_report_filename, validate_order)

    return (article, sheet_data, (xml_f, xml_e, xml_w), (data_f, data_e, data_w))


def validate_article_report_display(label, report_name, xml_stats, data_stats, xml_filename, doc_files_info):
    xml_f, xml_e, xml_w = xml_stats
    data_f, data_e, data_w = data_stats

    i = 0
    html = html_report.tag('h4', '-'*80)
    html += html_report.tag('h4', label)
    html += html_report.tag('h4', report_name)
    html += html_report.filecontent_in_collapsible_block(report_name, xml_filename, True)
    if xml_f + xml_e + xml_w > 0:
        i += 1
        content, style1 = html_report.filecontent_in_collapsible_block(report_name + str(i), doc_files_info.err_filename)
        html += content
        i += 1
        content, style2 = html_report.filecontent_in_collapsible_block(report_name + str(i), doc_files_info.style_report_filename)
        html += content

    if data_f + data_e + data_w > 0:
        i += 1
        content, style3 = html_report.filecontent_in_collapsible_block(report_name + str(i), doc_files_info.data_report_filename)
        html += content

    return (style1 + style2 + style3, html)


def validate_package(doc_files_info_list, dtd_files, report_path, validate_order, create_toc_report):
    index = 0
    n = '/' + str(doc_files_info_list)

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

        index += 1
        print(new_name)
        article, sheet_data, xml_stats, data_stats = validate_article_report_data(xml_filename, new_name, report_name, doc_files_info, dtd_files, validate_order)

        css, result_html = validate_article_report_display(str(index) + n, report_name, xml_stats, data_stats, xml_filename, doc_files_info)
        f, e, w = xml_stats
        xml_f += f
        xml_e += e
        xml_w += w

        f, e, w = data_stats
        data_f += f
        data_e += e
        data_w += w

        article_results[new_name] = (xml_stats, data_stats, result_html)

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
