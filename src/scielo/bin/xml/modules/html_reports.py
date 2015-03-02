# coding=utf-8

import os

from datetime import datetime

import xml_utils


def report_date():
    procdate = datetime.now().isoformat()
    return tag('h3', procdate[0:10] + ' ' + procdate[11:19])


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


def css_class(style):
    return ' class="' + style + '"' if style != '' else style


def collapsible_block(section_id, section_title, content):
    r = '<div id="show' + section_id + '" onClick="openClose(\'' + section_id + '\')" style="cursor:hand; cursor:pointer"><strong>' + section_title + ' (show)</strong></div>'
    r += '<div id="hide' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsiblehidden" style="cursor:hand; cursor:pointer"><strong>' + section_title + ' (hide) </strong></div>'
    r += '<div id="' + section_id + '" class="collapsible">'
    r += content
    r += '</div>'
    return r


def link(href, label):
    return '<a href="' + href + '">' + label + '</a>'


def tag(tag_name, content, style=''):
    if content is None:
        content = ''
    if tag_name == 'p' and '</p>' in content:
        tag_name = 'div'
    return '<' + tag_name + css_class(style) + '>' + content + '</' + tag_name + '>'


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
        element_name = 'span'
        stats = ' | '.join([k + ': ' + v for k, v in [('fatal errors', str(f)), ('errors', str(e)), ('warnings', str(w))]])
    else:
        element_name = 'div'
        stats = [('Total of fatal errors:', f), ('Total of errors:', e), ('Total of warnings:', w)]
        stats = ''.join([format_p_label_value(l, str(v)) for l, v in stats])

    text = 'FATAL ERROR' if f > 0 else 'ERROR' if e > 0 else 'WARNING' if w > 0 else ''
    style = message_style(text)
    if style == '' or style == 'ok':
        style = 'success'

    return tag(element_name, stats, style)


def display_links_to_report(files_list, path_relative=False):
    files = ''
    for item in files_list:
        if os.path.isfile(item):
            basename = os.path.basename(item)
            if path_relative is True:
                files += tag('p', link('file:///' + basename, basename))
            else:
                files += tag('p', link('file:///' + item, basename))
    if len(files) > 0:
        files = tag('p', 'Check the errors/warnings:') + files
    return files


def sheet(table_header_and_data, filename=None):
    table_header = None
    width = None

    if table_header_and_data is not None:
        table_header, wider, table_data = table_header_and_data

    r = '<p>'
    if table_header is None:
        r += '<!-- no data to create sheet -->'
    else:
        if len(table_header) > 2:
            width = 100
            width = 100 / len(table_header)
            width = str(width)

        r += '<table class="sheet">'
        r += '<thead><tr>'
        if filename is not None:
            r += '<th class="th"></th>'
        for label in table_header:
            r += '<th class="th">' + label + '</th>'
        r += '</tr></thead>'
        if len(table_data) == 0:
            r += '<tbody><tr>'
            for label in table_header:
                r += '<td>-</td>'
            r += '</tr></tbody>'
        else:
            r += '<tbody>'
            for row in table_data:
                r += '<tr>'
                if filename is not None:
                    r += '<td>' + filename + '</td>'

                for label in table_header:
                    r += '<td'
                    if label == '@id':
                        r += ' class="td_status"'
                    r += '>'
                    r += format_cell_data(row.get(label, ''), not label in ['filename', 'scope'], width) + '</td>'
                r += '</tr>'
            r += '</tbody>'
        r += '</table>'
    r += '</p>'
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
    if '</p>' in value:
        tag = 'div'
    else:
        tag = 'p'
    return '<' + tag + message_css_class(value) + '>' + value + '</' + tag + '>'


def format_list(label, list_type, list_items, style=''):
    r = ''
    r += '<div' + css_class(style) + '>'
    r += tag('p', (tag('span', label)))
    r += '<' + list_type + '>'
    if isinstance(list_items, dict):
        r += ''.join(['<li>' + display_label_value(k, v) + '</li>' for k, v in list_items.items()])
    elif isinstance(list_items, list):
        for item in list_items:
            if isinstance(item, dict):
                for k, v in item.items():
                    r += '<li>' + display_label_value(k, v) + '</li>'
            else:
                r += '<li>' + item + '</li>'
    r += '</' + list_type + '>'
    r += '</div>'
    return r


def format_cell_data(value, is_data, width=None):
    r = '-'
    if isinstance(value, list):
        r = ''
        r += '<ul>'
        for item in value:
            r += '<li>' + html_value(item) + '</li>'
        r += '</ul>'
    elif isinstance(value, dict):
        r = ''
        r += '<ul>'
        for k, v in value.items():
            if k != 'ordered':
                if isinstance(v, list):
                    r += '<li>' + k + ': ' + ', '.join(html_value(v)) + '</li>'
                else:
                    r += '<li>' + display_label_value(k, v) + '</li>'
        r += '</ul>'
    elif value is not None:
        # str or unicode
        r = html_value(value, width)
    if is_data:
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


def display_labeled_value(label, value, style='', element_name='p'):
    if label is None:
        label = 'None'
    return tag(element_name, tag('span', '[' + label + '] ', 'discret') + html_value(value), style)


def html_value(value, width=None):
    if value is None:
        value = 'None'
    if isinstance(value, int):
        value = str(value)
    if '<img' in value or '</a>' in value:
        pass
    else:
        if '<' in value and '>' in value:
            value = display_xml(value, width)
    return value


def message_style(value, default='ok'):
    r = default
    if 'FATAL ERROR' in value:
        r = 'fatalerror'
    elif 'ERROR' in value:
        r = 'error'
    elif 'WARNING' in value:
        r = 'warning'
    return r


def get_message_style(f, e, w):
    r = 'success'
    if f > 0:
        r = 'fatalerror'
    elif e > 0:
        r = 'error'
    elif w > 0:
        r = 'warning'
    return r


def message_css_class(style):
    return ' class="' + message_style(style) + '"'


def display_label_value(label, value):
    return tag('span', label) + ' ' + html_value(value)


def format_p_label_value(label, value):
    return tag('p', display_label_value(label, value))


def display_href(href, is_internal, is_image):
    r = ''
    if href is not None and href != '':
        if is_internal:
            _href = 'file:///' + href
            href = os.path.basename(href)
        else:
            _href = href
        if is_image:
            r = '<img src="' + _href + '"/>'
        else:
            r = '<a target="_blank" href="' + _href + '">' + href + '</a>'
    return r
