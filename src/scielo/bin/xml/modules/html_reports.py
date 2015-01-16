# coding=utf-8

import os

from datetime import datetime


def report_date():
    procdate = datetime.now().isoformat()
    return procdate[0:10] + ' ' + procdate[11:19]


def statistics(content, word):
    return len(content.split(word)) - 1


def statistics_numbers(content):
    e = statistics(content, 'ERROR')
    f = statistics(content, 'FATAL ERROR')
    e = e - f
    w = statistics(content, 'WARNING')
    return (f, e, w)


class ReportHTML(object):

    def __init__(self):
        self.title = ''
        self.body = ''

    def html(self):
        s = ''
        s += '<html>'
        s += '<head>'
        if isinstance(self.title, list):
            s += '<meta charset="utf-8"/><title>' + ' - '.join(self.title) + '</title>'
        else:
            s += '<meta charset="utf-8"/><title>' + self.title + '</title>'
        s += self.styles()
        s += '</head>'
        s += '<body>'
        s += self.report_date
        if isinstance(self.title, list):
            s += self.tag('h1', self.title[0])
            s += self.tag('h1', self.title[1])
        else:
            s += self.tag('h1', self.title)
        s += self.body
        s += '</body>'
        s += '</html>'

        return s

    def collapsible_block(self, section_id, section_title, content):
        r = '<div id="show' + section_id + '" onClick="openClose(\'' + section_id + '\')" style="cursor:hand; cursor:pointer">' + section_title + ' (show)</div>'
        r += '<div id="hide' + section_id + '" class="collapsiblehidden" style="cursor:hand; cursor:pointer"><b>' + section_title + ' (hide) </b></div>'
        r += '<div id="' + section_id + '" onClick="openClose(\'' + section_id + '\')" class="collapsible">'
        r += content
        r += '</div>'
        return r

    def statistics_messages(self, f, e, w, title='', files_list=[]):
        s = [('Total of fatal errors:', f), ('Total of errors:', e), ('Total of warnings:', w)]
        s = ''.join([self.format_p_label_value(l, str(v)) for l, v in s])

        text = 'FATAL ERROR' if f > 0 else 'ERROR' if e > 0 else 'WARNING' if w > 0 else ''
        style = self.message_style(text)
        if style == '' or style == 'ok':
            style = 'success'

        title = self.tag('h4', title) if title != '' else ''
        return self.tag('div', title + self.tag('div', s, style) + self.display_links_to_report(files_list), 'statistics')

    def display_links_to_report(self, files_list, path_relative=False):
        files = ''
        for item in files_list:
            if os.path.isfile(item):
                basename = os.path.basename(item)
                if path_relative is True:
                    files += self.tag('p', self.link('file:///' + basename, basename))
                else:
                    files += self.tag('p', self.link('file:///' + item, basename))
        if len(files) > 0:
            files = self.tag('p', 'Check the errors/warnings:') + files
        return files

    def body_section(self, style, anchor_name, title, content, sections=[]):
        anchor = anchor_name if anchor_name == '' else '<a name="' + anchor_name + '"/><a href="#top">^</a>'
        sections = '<ul class="sections">' + ''.join(['<li> [<a href="#' + s + '">' + t + '</a>] </li>' for s, t, d in sections]) + '</ul>'
        return anchor + '<' + style + '>' + title + '</' + style + '>' + sections + content

    def sheet(self, table_header_and_data, filename=None):
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
                        r += self.format_cell_data(row.get(label, ''), not label in ['filename', 'scope'], width) + '</td>'
                    r += '</tr>'
                r += '</tbody>'
            r += '</table>'
        r += '</p>'
        return r

    def link(self, href, label):
        return '<a href="' + href + '">' + label + '</a>'

    def tag(self, tag_name, content, style=''):
        if content is None:
            content = ''
        if tag_name == 'p' and '</p>' in content:
            tag_name = 'div'
        return '<' + tag_name + self.css_class(style) + '>' + content + '</' + tag_name + '>'

    def display_xml(self, value, width=None):
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        if width is not None:
            value = '<textarea cols="' + width + '" rows="10" readonly>' + value + '</textarea>'
        else:
            value = '<pre>' + value + '</pre>'
        return value

    def format_message(self, value):
        if '</p>' in value:
            tag = 'div'
        else:
            tag = 'p'
        return '<' + tag + self.message_css_class(value) + '>' + value + '</' + tag + '>'

    def css_class(self, style):
        return ' class="' + style + '"' if style != '' else style

    def format_list(self, label, list_type, list_items, style=''):
        r = ''
        r += '<div' + self.css_class(style) + '>'
        r += self.tag('p', (self.tag('span', label)))
        r += '<' + list_type + '>'
        if isinstance(list_items, dict):
            r += ''.join(['<li>' + self.display_label_value(k, v) + '</li>' for k, v in list_items.items()])
        elif isinstance(list_items, list):
            for item in list_items:
                if isinstance(item, dict):
                    for k, v in item.items():
                        r += '<li>' + self.display_label_value(k, v) + '</li>'
                else:
                    r += '<li>' + item + '</li>'
        r += '</' + list_type + '>'
        r += '</div>'
        return r

    def format_cell_data(self, value, is_data, width=None):
        r = '-'
        if isinstance(value, list):
            r = ''
            r += '<ul>'
            for item in value:
                r += '<li>' + self.html_value(item) + '</li>'
            r += '</ul>'
        elif isinstance(value, dict):
            r = ''
            r += '<ul>'
            for k, v in value.items():
                if k != 'ordered':
                    if isinstance(v, list):
                        r += '<li>' + k + ': ' + ', '.join(self.html_value(v)) + '</li>'
                    else:
                        r += '<li>' + self.display_label_value(k, v) + '</li>'
            r += '</ul>'
        elif value is not None:
            # str or unicode
            r = self.html_value(value, width)
        if is_data:
            r = self.format_message(r)
        return r

    def save(self, filename, title=None, body=None):
        if title is not None:
            self.title = title
        if body is not None:
            self.body = body

        f = open(filename, 'w')
        r = self.html()
        if isinstance(r, unicode):
            r = r.encode('utf-8')
        f.write(r)
        f.close()

    @property
    def report_date(self):
        return self.tag('h3', report_date())

    def display_labeled_value(self, label, value, style='', tag='p'):
        if label is None:
            label = 'None'
        return self.tag(tag, self.tag('span', '[' + label + '] ', 'discret') + self.html_value(value), style)

    def html_value(self, value, width=None):
        if value is None:
            value = 'None'
        if isinstance(value, int):
            value = str(value)
        if '<img' in value or '</a>' in value:
            pass
        else:
            if '<' in value and '>' in value:
                value = self.display_xml(value, width)
        return value

    def styles(self):
        css = '<style>' + open(os.path.dirname(os.path.realpath(__file__)) + '/report.css', 'r').read() + '</style>'
        js = open(os.path.dirname(os.path.realpath(__file__)) + '/collapsible.js', 'r').read()
        return css + js

    def message_style(self, value, default='ok'):
        r = default
        if 'FATAL ERROR' in value:
            r = 'fatalerror'
        elif 'ERROR' in value:
            r = 'error'
        elif 'WARNING' in value:
            r = 'warning'
        return r

    def message_css_class(self, style):
        return ' class="' + self.message_style(style) + '"'

    def display_label_value(self, label, value):
        return self.tag('span', label) + ' ' + self.html_value(value)

    def format_p_label_value(self, label, value):
        return self.tag('p', self.display_label_value(label, value))
