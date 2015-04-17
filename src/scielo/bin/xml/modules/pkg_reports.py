# coding=utf-8

import os
from datetime import datetime

import article_reports
import xpchecker
import html_reports


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def update_err_filename(err_filename, dtd_report):
    if os.path.isfile(dtd_report):
        separator = ''
        if os.path.isfile(err_filename):
            separator = '\n\n\n' + '.........\n\n\n'
        open(err_filename, 'a+').write(separator + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(dtd_report, 'r').read())


def delete_irrelevant_reports(ctrl_filename, is_valid_style, dtd_validation_report, style_checker_report):
    if ctrl_filename is None:
        if is_valid_style is True:
            os.unlink(style_checker_report)
    else:
        open(ctrl_filename, 'w').write('Finished')
    if os.path.isfile(dtd_validation_report):
        os.unlink(dtd_validation_report)


def get_article_xml_validations_reports(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename, run_background):

    xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, dtd_report, style_report, run_background)
    f, e, w = valid_style
    update_err_filename(err_filename, dtd_report)
    delete_irrelevant_reports(ctrl_filename, f + e + w == 0, dtd_report, style_report)
    if xml is None:
        f += 1
    if not valid_dtd:
        f += 1
    return (f, e, w)


def write_article_contents_validations_report(new_name, report_filename, content, display_title):

    f, e, w = html_reports.statistics_numbers(content)

    stats = ''
    title = ''
    if display_title:
        stats = html_reports.statistics_display(f, e, w, False)
        title = ['Contents validations required by SciELO ', new_name]

    html_reports.save(report_filename, title, stats + content)
    return (f, e, w)


def get_report_text(filename):
    report = ''
    if os.path.isfile(filename):
        content = open(filename, 'r').read()

        if 'Parse/validation finished' in content and '<!DOCTYPE' in content:
            part1 = content[0:content.find('<!DOCTYPE')]
            part2 = content[content.find('<!DOCTYPE'):]

            l = part1[part1.rfind('Line number:')+len('Line number:'):]
            l = l[0:l.find('Column')]
            l = ''.join([item.strip() for item in l.split()])
            if l.isdigit():
                l = str(int(l) + 1) + ':'
                if l in part2:
                    part2 = part2[0:part2.find(l)] + '\n...'

            part1 = part1.replace('\n', '<br/>')
            part2 = part2.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace('\t', '&nbsp;'*4)
            report = part1 + part2
        elif '</html>' in content:

            #report = '<iframe width="95%" height="400px" src="' + os.path.basename(filename) + '"></iframe>'
            content = open(filename, 'r').read()

            content = content[content.find('<body'):]
            content = content[0:content.rfind('</body>')]
            report = content[content.find('>')+1:]
        else:
            report = ''
    return report


def sum_stats(stats_items):
    f = sum([i[0] for i in stats_items])
    e = sum([i[1] for i in stats_items])
    w = sum([i[2] for i in stats_items])
    return (f, e, w)


def xml_list(pkg_path, xml_filenames=None):
    r = ''
    r += '<h2>XML files</h2>'
    r += '<p>XML path: ' + pkg_path + '</p>'
    if xml_filenames is None:
        xml_filenames = [pkg_path + '/' + name for name in os.listdir(pkg_path) if name.endswith('.xml')]
    r += '<p>Total of XML files: ' + str(len(xml_filenames)) + '</p>'
    r += html_reports.format_list('', 'ol', [os.path.basename(f) for f in xml_filenames])
    return r


def validate_package(articles, validate_order):
    return article_reports.toc_report_data(articles, validate_order)


def validate_pkg_items(org_manager, doc_items, doc_files_info_items, dtd_files, validate_order, display_all, xml_articles_status=None):
    articles_stats = {}
    articles_reports = {}
    articles_sheets = {}

    fatal_errors = 0

    for xml_name, doc_files_info in doc_files_info_items.items():
        for f in [doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename, doc_files_info.pmc_style_report_filename]:
            if os.path.isfile(f):
                os.unlink(f)

    print('Validating package: inicio')
    register_log('pkg_reports.validate_pkg_items: inicio')
    for xml_name in sorted_xml_name_by_order(doc_items):
        doc = doc_items[xml_name]
        doc_files_info = doc_files_info_items[xml_name]

        skip = False
        if xml_articles_status is not None:
            skip = xml_articles_status[doc_files_info.xml_name] == 'skip-update'
        if not skip:
            new_name = doc_files_info.new_name
            xml_filename = doc_files_info.new_xml_filename
            print(new_name)
            register_log(new_name)

            register_log('pkg_reports.validate_pkg_items: get_article_xml_validations_reports')
            print(datetime.now().isoformat() + ' validating xml')
            xml_f, xml_e, xml_w = get_article_xml_validations_reports(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename, display_all is False)

            print(datetime.now().isoformat() + ' validating contents')
            register_log('pkg_reports.validate_pkg_items: get_article_contents_validations_report')

            content, sheet_data, _log_items = article_reports.get_report_content(org_manager, doc, new_name, os.path.dirname(xml_filename), validate_order, display_all)
            print(datetime.now().isoformat() + ' writing contents validations report')
            data_f, data_e, data_w = write_article_contents_validations_report(new_name, doc_files_info.data_report_filename, content, display_all)

            articles_stats[new_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))

            fatal_errors += xml_f + data_f

            articles_reports[new_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)

            register_log('pkg_reports.validate_pkg_items: authors_sheet_data ...')
            if sheet_data is not None:
                print(datetime.now().isoformat() + ' creating lists')
                articles_sheets[new_name] = (sheet_data.authors_sheet_data(new_name), sheet_data.sources_sheet_data(new_name))
                print(datetime.now().isoformat() + ' lists created')
            else:
                articles_sheets[new_name] = (None, None)

    register_log('pkg_reports.validate_pkg_items: fim')
    print('Validating package: fim')
    return (fatal_errors, articles_stats, articles_reports, articles_sheets)


def get_toc_report_text(toc_f, toc_e, toc_w, toc_report):
    toc_text = ''
    if toc_f + toc_e + toc_w > 0:
        toc_text = html_reports.tag('h2', 'Table of contents Report')
        toc_text += html_reports.collapsible_block('toc', 'table of contents validations: ' + html_reports.statistics_display(toc_f, toc_e, toc_w), toc_report, html_reports.get_stats_numbers_style(toc_f, toc_e, toc_w))
    return toc_text


def label_values(labels, values):
    r = {}
    for i in range(0, len(labels)):
        r[labels[i]] = values[i]
    return r


def articles_sorted_by_order(articles):
    sorted_by_order = {}
    for xml_name, article in articles.items():
        if not article.order in sorted_by_order.keys():
            sorted_by_order[article.order] = []
        sorted_by_order[article.order].append(article)
    return sorted_by_order


def sorted_xml_name_by_order(articles):
    order_and_xml_name_items = {}
    for xml_name, article in articles.items():
        if not article.order in order_and_xml_name_items.keys():
            order_and_xml_name_items[article.order] = []
        order_and_xml_name_items[article.order].append(xml_name)

    sorted_items = []
    for order in sorted(order_and_xml_name_items.keys()):
        for item in order_and_xml_name_items[order]:
            sorted_items.append(item)
    return sorted_items


def get_articles_report_text(articles_reports, articles_stats):
    n = '/' + str(len(articles_reports))
    validations_text = ''
    index = 0
    validations_text = html_reports.tag('h2', 'XML Validations')
    for new_name in sorted(articles_reports.keys()):
        index += 1
        item_label = str(index) + n + ' - ' + new_name
        print(item_label)
        validations_text += html_reports.tag('h4', item_label)
        xml_f, xml_e, xml_w = articles_stats[new_name][0]
        data_f, data_e, data_w = articles_stats[new_name][1]

        rep1, rep2, rep3 = articles_reports[new_name]
        if xml_f + xml_e + xml_w > 0:
            t = []
            v = []
            for rep in [rep1, rep2]:
                content = get_report_text(rep)
                if len(content) > 0:
                    t.append(os.path.basename(rep))
                    v.append(content)
            content = ''.join(v)
            s = html_reports.statistics_display(xml_f, xml_e, xml_w)
            validations_text += html_reports.collapsible_block('xmlrep' + str(index), 'XML validations (' + ' and '.join(t) + '): ' + s, content, html_reports.get_stats_numbers_style(xml_f, xml_e, xml_w))

        if data_f + data_e + data_w > 0:
            s = html_reports.statistics_display(data_f, data_e, data_w)
            validations_text += html_reports.collapsible_block('datarep' + str(index), 'Contents validations (' + os.path.basename(rep3) + '): ' + s, get_report_text(rep3), html_reports.get_stats_numbers_style(data_f, data_e, data_w))

    return validations_text


def get_lists_report_text(articles_reports, articles_sheets):
    toc_authors_sheet_data = []
    toc_sources_sheet_data = []
    authors_h = None
    authors_w = None
    sources_h = None
    sources_w = None

    lists_text = html_reports.tag('h2', 'Authors and Sources Lists')

    for new_name in sorted(articles_reports.keys()):
        if not articles_sheets[new_name][0] is None:
            authors_h, authors_w, authors_data = articles_sheets[new_name][0]
            toc_authors_sheet_data += authors_data

        if not articles_sheets[new_name][1] is None:
            sources_h, sources_w, sources_data = articles_sheets[new_name][1]
            toc_sources_sheet_data += sources_data

    authors = html_reports.sheet(authors_h, authors_w, toc_authors_sheet_data)
    lists_text += html_reports.collapsible_block('authors', 'Authors in the package', authors)

    sources = html_reports.sheet(sources_h, sources_w, toc_sources_sheet_data)
    lists_text += html_reports.collapsible_block('sources', 'Sources in the package', sources)

    return lists_text


def processing_result_location(result_path):
    return 'Result of the processing: ' + html_reports.link('file:///' + result_path, result_path)


def save_report(filename, title, content):
    html_reports.save(filename, title, content)
    print('\n\nReport:\n ' + filename)


def display_report(report_filename):
    try:
        os.system('python -mwebbrowser file:///' + report_filename.replace('//', '/'))
    except:
        pass
