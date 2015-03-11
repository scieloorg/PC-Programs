# coding=utf-8

import os

import article_reports
import xpchecker
import html_reports


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


def get_article_xml_validations_reports(new_name, xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename):

    print('validating xml')
    xml, valid_dtd, valid_style = xpchecker.validate_article_xml(xml_filename, dtd_files, dtd_report, style_report)
    f, e, w = valid_style
    update_err_filename(err_filename, dtd_report)
    delete_irrelevant_reports(ctrl_filename, f + e + w == 0, dtd_report, style_report)
    if xml is None:
        f += 1
    if not valid_dtd:
        w += 1
    return (f, e, w)


def get_article_contents_validations_report(article, new_name, package_path, report_filename, validate_order, display_title):
    content, sheet_data = article_reports.get_report_content(article, new_name, package_path, validate_order, display_title)

    f, e, w = html_reports.statistics_numbers(content)

    stats = ''
    title = ''
    if display_title:
        stats = html_reports.statistics_display(f, e, w, False)
        title = ['Contents validations required by SciELO ', new_name]

    html_reports.save(report_filename, title, stats + content)

    return (f, e, w, sheet_data)


def get_report_text(filename, status):
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

            report = '<iframe width="95%" height="400px" src="file:///' + filename + '"></iframe>'

            #content = content[content.find('<body'):]
            #content = content[0:content.rfind('</body>')]
            #report = content[content.find('>')+1:]
        else:
            report = ''
    if len(report) > 0:
        report = '<div class="embedded-report-' + status + '"><h5>' + filename + '</h5>' + report + '</div>'
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


def validate_pkg_items(pkg_items, dtd_files, validate_order, display_all):
    articles_stats = {}
    articles_reports = {}
    articles_sheets = {}

    print('Validating package')
    for doc, doc_files_info in pkg_items:
        new_name = doc_files_info.new_name
        xml_filename = doc_files_info.new_xml_filename
        print(new_name)
        xml_f, xml_e, xml_w = get_article_xml_validations_reports(new_name, xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)

        data_f, data_e, data_w, sheet_data = get_article_contents_validations_report(doc, new_name, os.path.dirname(xml_filename), doc_files_info.data_report_filename, validate_order, display_all)

        articles_stats[new_name] = ((xml_f, xml_e, xml_w), (data_f, data_e, data_w))
        articles_reports[new_name] = (doc_files_info.err_filename, doc_files_info.style_report_filename, doc_files_info.data_report_filename)
        if sheet_data is not None:
            articles_sheets[new_name] = (sheet_data.authors_sheet_data(new_name), sheet_data.sources_sheet_data(new_name))
        else:
            articles_sheets[new_name] = (None, None)

    return (articles_stats, articles_reports, articles_sheets)


def get_toc_report_text(toc_f, toc_e, toc_w, toc_report):
    toc_text = ''
    if toc_f + toc_e + toc_w > 0:
        toc_text = html_reports.tag('h2', 'Table of contents Report')
        toc_text += html_reports.collapsible_block('toc', 'table of contents validations ' + html_reports.statistics_display(toc_f, toc_e, toc_w), toc_report)
    return toc_text


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
                content = get_report_text(rep, html_reports.get_message_style(xml_f, xml_e, xml_w))
                if len(content) > 0:
                    t.append(os.path.basename(rep))
                    v.append(content)
            content = ''.join(v)
            s = html_reports.statistics_display(xml_f, xml_e, xml_w)
            validations_text += html_reports.collapsible_block('xmlrep' + str(index), s + ' - XML validations - ' + ' and '.join(t), content)

        if data_f + data_e + data_w > 0:
            s = html_reports.statistics_display(data_f, data_e, data_w)
            validations_text += html_reports.collapsible_block('datarep' + str(index), s + ' - contents validations - ' + os.path.basename(rep3), get_report_text(rep3, html_reports.get_message_style(data_f, data_e, data_w)))

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

    authors = html_reports.sheet((authors_h, authors_w, toc_authors_sheet_data))
    lists_text += html_reports.collapsible_block('authors', 'Authors in the package', authors)

    sources = html_reports.sheet((sources_h, sources_w, toc_sources_sheet_data))
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
