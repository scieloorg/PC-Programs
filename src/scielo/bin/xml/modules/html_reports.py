# coding=utf-8

import os

from datetime import datetime

import xml_utils


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
    css = '<style>' + open(os.path.dirname(os.path.realpath(__file__)) + '/report.css', 'r').read() + '</style>'
    js = open(os.path.dirname(os.path.realpath(__file__)) + '/collapsible.js', 'r').read()
    return css + js


def body_section(style, anchor_name, title, content, sections=[]):
    anchor = anchor_name if anchor_name == '' else '<a name="' + anchor_name + '"/><a href="#top">^</a>'
    sections = '<ul class="sections">' + ''.join(['<li> [<a href="#' + s + '">' + t + '</a>] </li>' for s, t, d in sections]) + '</ul>'
    return anchor + '<' + style + '>' + title + '</' + style + '>' + sections + content


def attr(name, value):
    return ' ' + name + '="' + value + '"' if value is not None and name is not None else ''


def collapsible_block(section_id, section_title, content, status='ok'):
    r = '<div id="show' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsiblehidden" style="cursor:hand; cursor:pointer"><strong>' + section_title + ' [+]</strong></div>'
    r += '<div id="hide' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsibleopen" style="cursor:hand; cursor:pointer"><strong>' + section_title + ' [-] </strong></div>'
    r += '<div id="' + section_id + '" class="collapsibleopen">'
    r += '<div class="embedded-report-' + status + '">' + content + '</div>'
    r += '</div>'
    return r


def link(href, label):
    return '<a href="' + href + '">' + label + '</a>'


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


def statistics_display(f, e, w, inline=True):
    if inline:
        tag_name = 'span'
        stats = ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(f)), ('errors', str(e)), ('warnings', str(w))]])
    else:
        tag_name = 'div'
        stats = [('Total of fatal errors:', f), ('Total of errors:', e), ('Total of warnings:', w)]
        stats = ''.join([tag('p', display_label_value(l, str(v))) for l, v in stats])
    return tag(tag_name, stats, get_stats_numbers_style(f, e, w))


def sheet(table_header, wider, table_data, filename=None, table_style='sheet', row_style=None):
    r = ''
    width = None
    if not table_header is None:
        if len(table_header) > 3:
            width = 800
            width = 800 / len(table_header)
            width = str(width)

        th = ''
        if filename is not None:
            th += '<th class="th"></th>'
        for label in table_header:
            th += tag('th', label, 'th')

        if len(table_data) == 0:
            tr = ''
            if filename is not None:
                tr += '<td></td>'
            for label in table_header:
                tr += '<td>-</td>'
            tbody = tag('tr', tr)

        else:
            tbody = ''
            if table_style == 'sheet':
                for row in table_data:
                    tr = ''
                    if filename is not None:
                        tr += tag('td', filename)

                    for label in table_header:
                        cell_style = 'td_status' if label == '@id' else None
                        cell_content = format_html_data(row.get(label, ''), not label in ['filename', 'scope', 'label', 'status'], width)
                        tr += tag('td', cell_content, cell_style)
                    tbody += tag('tr', tr)
            else:
                cell_style_prefix = 'td_' if row_style == 'status' else ''
                for row in table_data:
                    tr = ''
                    for label in table_header:
                        cell_content = format_html_data(row.get(label, ''))
                        cell_style = cell_style_prefix + label
                        if cell_style == label:
                            cell_style = get_message_style(row.get(label), None)
                        tr += tag('td', cell_content, cell_style)
                    tr_style = None
                    if row_style == 'status':
                        tr_style = get_message_style(row.get(row_style), None)
                    tbody += tag('tr', tr, tr_style)

        r = tag('p', tag('table', tag('thead', tag('tr', th)) + tag('tbody', tbody), table_style))
    return r


def display_xml(value, width=None):
    value = xml_utils.pretty_print(value)
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    if width is not None:
        value = '<textarea cols="' + width + '" rows="10" readonly>' + value + '</textarea>'
    else:
        value = '<pre>' + value + '</pre>'
    return value


def format_message(value):
    return tag('p', value, get_message_style(value, 'ok'))


def li_from_dict(list_items):
    li_items = ''
    for k, v in list_items.items():
        if isinstance(v, list):
            #FIXME format_html_data?
            v = ', '.join(v)
        li_items += tag('li', display_label_value(k, v))
    return li_items


def format_list(label, list_type, list_items, style=''):
    if isinstance(list_items, dict):
        ltype = list_type
        li_items = li_from_dict(list_items)
    elif isinstance(list_items, list):
        ltype = 'ol'
        li_items = ''
        for item in list_items:
            li = item
            if isinstance(item, dict):
                li = format_list(label, list_type, item, style)
            li_items += tag('li', li)
    return tag('div', tag('p', label, 'label') + tag(ltype, li_items), style)


def format_html_data(value, apply_message_style=False, width=None):
    r = '-'
    if isinstance(value, list):
        r = format_list('', 'ol', value)
    elif isinstance(value, dict):
        r = format_list('', 'ul', value)
    elif value is None:
        # str or unicode
        r = '-'
    elif isinstance(value, int):
        r = str(value)
    else:
        if '<img' in value or '</a>' in value:
            r = value
        else:
            if '<' in value and '>' in value:
                r = display_xml(value, width)
            else:
                r = value
    if apply_message_style:
        r = format_message(r)
    return r


def save(filename, title, body):
    if title is not None:
        title = title
    if body is not None:
        body = body

    f = open(filename, 'w')
    r = html(title, body)
    if isinstance(r, unicode):
        r = r.encode('utf-8')
    f.write(r)
    f.close()


def get_message_style(value, default):
    if value is None:
        value = ''
    if 'FATAL ERROR' in value:
        r = 'fatalerror'
    elif 'ERROR' in value:
        r = 'error'
    elif 'WARNING' in value:
        r = 'warning'
    elif default is None:
        r = value
    else:
        r = default
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
    return tag('p', tag('span', '[' + label + '] ', 'discret') + format_html_data(value), style)


def display_label_value(label, value):
    return tag('span', label, 'label') + ': ' + format_html_data(value)


def image(path):
    return '<img src="' + path + '"/>'
