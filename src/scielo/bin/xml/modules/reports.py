# code = utf-8

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

    def statistics_messages(self, f, e, w, title):
        s = [('Total of fatal errors:', f), ('Total of errors:', e), ('Total of warnings:', w)]
        s = ''.join([self.format_p_label_value(l, str(v)) for l, v in s])

        text = 'FATAL ERROR' if f > 0 else 'ERROR' if e > 0 else 'WARNING' if w > 0 else ''
        style = self.message_style(text)
        if style == '' or style == 'ok':
            style = 'success'
        return self.tag('h3', title) + self.format_div(self.format_div(s, style), 'statistics')

    def body_section(self, style, anchor_name, title, content, sections=[]):
        anchor = anchor_name if anchor_name == '' else '<a name="' + anchor_name + '"/><a href="#top">^</a>'
        sections = '<ul class="sections">' + ''.join(['<li> [<a href="#' + s + '">' + t + '</a>] </li>' for s, t, d in sections]) + '</ul>'
        return anchor + '<' + style + '>' + title + '</' + style + '>' + sections + content

    def sheet(self, table_header_and_data, filename=None):
        table_header, wider, table_data = table_header_and_data
        r = '<p>'
        if table_header is None:
            r += '<!-- no data to create sheet -->'
        else:
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
                        r += '<td>' + self.format_cell(row.get(label, ''), not label in ['filename', 'scope']) + '</td>'
                    r += '</tr>'
                r += '</tbody>'
            r += '</table>'
        r += '</p>'
        return r

    def link(self, href, label):
        return '<a href="' + href + '">' + label + '</a>'

    def format_div(self, content, style=''):
        return self.tag('div', content, style)

    def tag(self, tag_name, content, style=''):
        if tag_name == 'p' and '</p>' in content:
            tag_name = 'div'
        if content is None:
            content = 'None'
        elif content.isdigit():
            content = str(content)
        return '<' + tag_name + self.css_class(style) + '>' + content + '</' + tag_name + '>'

    def display_xml(self, value):
        if value is None:
            value = ''
        value = value.replace('<pre>', '').replace('</pre>', '')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        return '<pre>' + value + '</pre>'

    def display_xml_in_small_space(self, value, width='100'):
        if value is None:
            value = ''
        value = value.replace('<pre>', '').replace('</pre>', '')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        return '<textarea cols="' + width + '" rows="10" readonly>' + value + '</textarea>'

    def format_message(self, value):
        if '<p' in value:
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

    def format_cell(self, value, is_data=True):
        def format_data(data, is_data):
            if is_data:
                if '<pre>' in data and '</pre>' in data:
                    data = self.display_xml(data)
                style = self.message_style(data, 'value')
                return self.tag('span', data, style)
            else:
                return data

        r = '-'
        if isinstance(value, list):
            r = ''
            r += '<ul>'
            for item in value:
                r += '<li>' + format_data(item, is_data) + '</li>'
            r += '</ul>'
        elif isinstance(value, dict):
            r = ''
            r += '<ul>'
            for k, v in value.items():
                if k != 'ordered':
                    if isinstance(v, list):
                        r += '<li>' + k + ': ' + ', '.join(format_data(v, is_data)) + '</li>'
                    else:
                        r += '<li>' + self.display_label_value(k, format_data(v, is_data)) + '</li>'
            r += '</ul>'
        elif value is not None:
            # str or unicode
            r = format_data(value, is_data)
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

    def display_value_with_discret_label(self, label, value, style='', tag='p'):
        if value is None:
            value = 'None'
        return self.tag(tag, self.tag('span', '[' + label + '] ', 'discret') + value, style)

    def styles(self):
        return '<style>' + open(os.path.dirname(os.path.realpath(__file__)) + '/report.css', 'r').read() + '</style>'

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
        r = value if value is not None else 'None'
        return self.tag('span', label) + ' ' + r

    def format_p_label_value(self, label, value):
        return self.tag('p', self.display_label_value(label, value))

    def display_attributes(self, label, attributes):
        r = []
        for key, value in attributes.items():
            if value is list:
                value = '; '.join(value)
            r.append(self.display_label_value(key, value))
        return label + '\n' + '\n'.join(r) + '\n'

    def display_items_with_attributes(self, label, items_with_attributes):
        r = label + ': ' + '\n'
        for item_name, item_values in items_with_attributes.items():
            r += self.display_label_values_with_attributes(item_name, item_values)
        return r + '\n'

    def display_label_values_with_attributes(self, label, values_with_attributes):
        return label + ': ' + '\n' + '\n'.join([self.display_attributes('=>', item) for item in values_with_attributes]) + '\n'

    def conditional_required(self, label, value):
        return self.display_label_value(label, value) if value is not None else 'WARNING: Required ' + label + ', if exists. '

    def required(self, label, value):
        return self.display_label_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def required_one(self, label, value):
        return self.display_attributes(label, value) if value is not None else 'ERROR: Required ' + label + '. '

    def expected_values(self, label, value, expected):
        return self.display_label_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)

    def add_new_value_to_index(self, dict_key_and_values, key, value):
        if key is not None:
            if not key in dict_key_and_values.keys():
                dict_key_and_values[key] = []
            dict_key_and_values[key].append(value)
        return dict_key_and_values
