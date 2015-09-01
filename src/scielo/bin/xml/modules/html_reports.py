# coding=utf-8

import os

from datetime import datetime

from __init__ import _
import xml_utils


XML_WIDTH = 140


def validations_table(results):
    r = ''
    if results is not None:
        rows = []
        for label, status, msg in results:
            rows.append({'label': label, 'status': status, 'message': msg})
        r = tag('div', sheet(['label', 'status', 'message'], rows, table_style='validation', row_style='status'))
    return r


def report_date():
    procdate = datetime.now().isoformat()
    return tag('p', procdate[0:10] + ' ' + procdate[11:19], 'report-date')


def statistics(content, word):
    return len(content.split(word)) - 1


def statistics_numbers(content):
    e = statistics(content, 'ERROR')
    f = statistics(content, 'FATAL ERROR')
    e = e - f
    w = statistics(content, 'WARNING')
    return (f, e, w)


def get_unicode(text):
    if text is None:
        text = u''
    if not isinstance(text, unicode):
        try:
            text = text.decode('utf-8')
        except Exception as e:
            try:
                text = text.decode('utf-8', 'xmlcharrefreplace')
            except Exception as e:
                print(e)
                print(text)
                #text = u''
    return text


def join_texts(texts):
    text = u''.join([get_unicode(t) for t in texts])
    return text


def styles():
    css = '<style>' + open(os.path.dirname(os.path.realpath(__file__)) + '/html_reports.css', 'r').read() + '</style>'
    js = open(os.path.dirname(os.path.realpath(__file__)) + '/html_reports_collapsible.js', 'r').read()
    return css + js


def body_section(style, anchor_name, title, content, sections=[]):
    anchor = anchor_name if anchor_name == '' else '<a name="' + anchor_name + '"/><a href="#top">^</a>'
    sections = '<ul class="sections">' + ''.join(['<li> [<a href="#' + s + '">' + t + '</a>] </li>' for s, t, d in sections]) + '</ul>'
    return anchor + '<' + style + '>' + title + '</' + style + '>' + sections + content


def attr(name, value):
    return ' ' + name + '="' + value + '"' if value is not None and name is not None else ''


def collapsible_block(section_id, section_title, content, status='ok'):
    r = '<a name="begin_' + section_id + '"/><div id="show' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsiblehidden" style="cursor:hand; cursor:pointer">' + section_title + ' <span class="button">[+]</span></div>'
    r += '<div id="hide' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsibleopen" style="cursor:hand; cursor:pointer">' + section_title + '<span class="button">[-]</span></div>'
    r += '<div id="' + section_id + '" class="collapsibleopen">'
    r += '<div class="embedded-report-' + status + '">' + content + '</div>'
    r += '<div class="endreport">'
    r += '  <div>' + ' ~ '*10 + 'end of report ' + ' ~ '*10 + '</div>'
    r += '  <div onClick="openClose(\'' + section_id + '\')" style="cursor:hand; cursor:pointer"><span class="button"> [ close ] </span></div>'
    r += '</div>'
    r += '</div>'

    return r


def link(href, label):
    return '<a href="' + href + '" target="_blank">' + label + '</a>'


def tag(tag_name, content, style=None):
    if content is None:
        content = ''
    if tag_name == 'p' and '</p>' in content:
        tag_name = 'div'
    return '<' + tag_name + attr('class', style) + '>' + content + '</' + tag_name + '>'


def html(title, body):
    s = ''
    s += '<html>'
    s += '<head>'
    if isinstance(title, list):
        s += '<meta charset="utf-8"/><title>' + ' - '.join(title) + '</title>'
    else:
        s += '<meta charset="utf-8"/><title>' + title + '</title>'
    s += styles()
    s += '</head>'
    s += '<body>'
    s += report_date()
    if isinstance(title, list):
        s += tag('h1', title[0])
        s += tag('h1', title[1])
    else:
        s += tag('h1', title)
    s += body
    s += '</body>'
    s += '</html>'

    return s


def statistics_display(validations_results, inline=True):
    if inline:
        tag_name = 'span'
        stats = ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(validations_results.fatal_errors)), ('errors', str(validations_results.errors)), ('warnings', str(validations_results.warnings))]])
    else:
        tag_name = 'div'
        stats = [('Total of fatal errors', validations_results.fatal_errors), ('Total of errors', validations_results.errors), ('Total of warnings', validations_results.warnings)]
        stats = ''.join([tag('p', display_label_value(l, str(v))) for l, v in stats])
    return tag(tag_name, stats, get_stats_numbers_style(validations_results.fatal_errors, validations_results.errors, validations_results.warnings))


def cell_width(table_header):
    width = XML_WIDTH
    if len(table_header) > 1:
        width = XML_WIDTH / len(table_header)
    if width < 30:
        width = 30
    if len(table_header) == 3:
        width = XML_WIDTH / 2
    return width


def sheet(table_header, table_data, table_style='sheet', row_style=None, html_cell_content=[]):
    r = ''
    if not table_header is None:
        width = cell_width(table_header)

        th = ''.join([tag('th', label, 'th') for label in table_header])

        if len(table_data) == 0:
            tbody = tag('tr', ''.join(['<td>-</td>' for label in table_header]))
        else:
            cell_style_prefix = 'td_' if table_style == 'validation' else ''
            tbody = ''

            for row in table_data:
                tr = ''
                if len(row) == len(table_header):
                    for label in table_header:
                        # cell content
                        cell_content = row.get(label, '')
                        if not label in html_cell_content:
                            cell_content = format_html_data(cell_content, width)
                        if table_style == 'sheet':
                            cell_content = color_text(cell_content)

                        # cell style
                        cell_style = 'td_status' if label == '@id' else cell_style_prefix + label
                        if cell_style == label:
                            cell_style = get_message_style(row.get(label), label)

                        tr += tag('td', cell_content, cell_style)
                elif len(row) == 1:
                    # hidden tr
                    tr += '<td colspan="' + str(len(table_header)) + '" class="' + label + '-hidden-block">' + row.get(label, '') + '</td>'

                # row style
                tr_style = None
                if row_style is not None:
                    tr_style = get_message_style(row.get(row_style), '')
                tbody += tag('tr', tr, tr_style)
        r = tag('p', tag('table', tag('thead', tag('tr', th)) + tag('tbody', tbody), table_style))
    return r


def display_xml(value, width=30):
    value = xml_utils.pretty_print(value)
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')

    rows_count = len(value) / width
    if rows_count > 10:
        rows_count = 10
    return '<textarea cols="' + str(width) + '" rows="' + str(rows_count) + '" readonly>' + value + '</textarea>'


def p_message(value):
    return tag('p', value, get_message_style(value, 'ok'))


def color_text(value):
    return tag('span', value, get_message_style(value, 'ok'))


def format_list(label, list_type, list_items, style=''):
    if isinstance(list_items, dict):
        list_items = format_html_data_dict(list_items, list_type)
    elif isinstance(list_items, list):
        li_items = format_html_data_list(list_items, list_type)
    return tag('div', tag('p', label, 'label') + li_items, style)


def format_html_data_dict(value, list_type='ul'):
    r = '<' + list_type + '>'
    for k, v in value.items():
        r += tag('li', display_label_value(k, v))
    r += '</' + list_type + '>'
    return r


def format_html_data_list(value, list_type='ol'):
    r = '<' + list_type + '>'
    for v in value:
        r += tag('li', format_html_data(v))
    r += '</' + list_type + '>'
    return r


def format_html_data(value, width=30):
    r = '-'
    if isinstance(value, list):
        r = format_html_data_list(value)
    elif isinstance(value, dict):
        r = format_html_data_dict(value)
    elif value is None:
        # str or unicode
        r = '-'
    elif isinstance(value, int):
        r = str(value)
    elif '<OPTIONS/>' in value:
        msg, value = value.split('<OPTIONS/>')
        value = value.split('|')
        r = msg + '<select size="10">' + '\n'.join(['<option>' + op + '</option>' for op in sorted(value)]) + '</select>'
    elif '<img' in value or '</a>' in value:
        r = value
    elif '<' in value and '>' in value:
        r = display_xml(value, width)
    else:
        r = value
    return r


def save(filename, title, body):
    if title is not None:
        title = title
    if body is not None:
        body = body
    r = html(title, body)
    if isinstance(r, unicode):
        r = r.encode('utf-8')
    open(filename, 'w').write(r)


def get_message_style(value, default):
    if value is None:
        value = ''
    if 'FATAL ERROR' in value:
        r = 'fatalerror'
    elif 'ERROR' in value:
        r = 'error'
    elif 'WARNING' in value:
        r = 'warning'
    elif default is None or default == '':
        r = value
    else:
        r = default
    if r is not None:
        r = r.replace(' ', '-').replace('@', '')
    return r


def get_stats_numbers_style(f, e, w):
    r = 'success'
    if f > 0:
        r = 'fatalerror'
    elif e > 0:
        r = 'error'
    elif w > 0:
        r = 'warning'
    return r


def display_labeled_value(label, value, style=''):
    if label is None:
        label = 'None'
    return tag('p', tag('span', '[' + label + '] ', 'discret') + format_html_data(value, XML_WIDTH), style)


def display_label_value(label, value):
    return tag('span', label, 'label') + ': ' + format_html_data(value)


def image(path):
    return '<img src="' + path + '"/>'


def section(title, content):
    r = '<div class="report-section">'
    r += '<h2>' + title + '</h2>'
    r += content
    r += '</div>'
    return r


def tab_block(tab_id, content, status='not-selected-tab-content'):
    if content is None:
        content = ''
    r = '<div id="tab-content-' + tab_id + '" class="' + status + '">'
    r += content
    r += '</div>'
    return r


def tabs_items(tabs, selected):
    r = ''
    for tab_id, tab_label in tabs:
        style = 'not-selected-tab'
        if tab_id == selected:
            style = 'selected-tab'
        r += '<span id="tab-label-' + tab_id + '"  onClick="display_tab_content(\'' + tab_id + '\', \'' + selected + '\')" class="' + style + '">' + tab_label + '</span>'
    return '<div class="tabs">' + r + '</div>'


def report_link(report_id, report_label, style, location):
    return '<a name="begin_label-' + report_id + '"/>&#160;<p id="label-' + report_id + '" onClick="display_article_report(\'' + report_id + '\', \'label-' + report_id + '\', \'' + location + '\')" class="report-link-' + style + '">' + report_label.replace(' ', '&#160;') + '</p>'


def report_block(report_id, content, style, location):
    r = '<div id="' + report_id + '" class="report-block-' + style + '">'
    r += content
    r += '<div class="endreport"><span class="button" onClick="display_article_report(\'' + report_id + '\', \'label-' + report_id + '\', \'' + location + '\')"> ' + _('close') + ' </span></div>'
    r += '</div>'
    return r
