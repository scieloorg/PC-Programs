# coding=utf-8
import difflib
from datetime import datetime


IMDEBUGGING = False


def now():
    now = datetime.now().isoformat().replace('-', '').replace(':', '').replace('T', ' ')[0:13]
    return now.split(' ')


def compare_text(str1, str2):
    str1 = str1 or ''
    str2 = str2 or ''

    s1 = [item for item in str1.upper().split() if item]
    s2 = [item for item in str2.upper().split() if item]
    return s1 == s2


def display_datetime(dateiso, timeiso=None):
    if dateiso is None:
        return ''
    if len(dateiso) < 8:
        return ''
    y = dateiso[:4]
    m = dateiso[4:6]
    d = dateiso[6:8]
    r = '/'.join([item for item in [d, m, y] if int(item) > 0])
    if timeiso is not None:
        if len(timeiso) > 0:
            r += ' ' + ':'.join([timeiso[i*2:i*2+2] for i in range(0, 2)])
    return r


def is_similar(text, items, min_rate=0.8):
    if not isinstance(items, list):
        items = [items]
    highiest_rate, most_similar_items = most_similar(similarity(items, text, min_rate))
    return (highiest_rate > min_rate)


def how_similar(this, that):
    if this is None:
        this = 'None'
    if that is None:
        that = 'None'
    return difflib.SequenceMatcher(None, this.lower(), that.lower()).ratio()


def similarity(items, text, min_ratio=0):
    r = {}
    for item in items:
        rate = how_similar(item, text)
        if rate > min_ratio:
            if rate not in r.keys():
                r[rate] = []
            r[rate].append(item)
    return r


def most_similar(similarity):
    items = []
    highiest_rate = 0
    ratio_list = similarity.keys()
    if len(ratio_list) > 0:
        ratio_list = sorted(ratio_list)
        ratio_list.reverse()
        highiest_rate = ratio_list[0]
        items = similarity[highiest_rate]

    return (highiest_rate, items)


def valid_formula_min_max_height(values, percent=0.25):
    m = 0
    if len(values) > 0:
        m = values[int(len(values)/2)]
    r = int(m * percent)
    _min = m - r
    _max = m + r
    if _min < 16:
        m = 16 + r
    if _max > 200:
        m = 200 - r
    return (m - r, m + r)


def diff(sentence1, sentence2):
    s1 = sentence1
    sentence1 = sentence1.split()

    d1 = [item for item in sentence1 if item not in sentence2.split()]

    if len(d1) > 0:
        equal = []
        s1 = []
        s2 = []
        for item in sentence1:
            if item in d1:
                item = ' **' + item + '** '
                equal.append(' '.join(s2))
                s2 = []
            else:
                s2.append(item)
            s1.append(item)
        s1 = ' '.join(s1)

    return [d1, s1]


def repl(matchobj):
    return matchobj.group(0).replace(matchobj.group(1), u'')


class RSTTable(object):

    def __init__(self, table_header, table_data):
        self.table_data = table_data
        self.table_header = table_header

    @property
    def columns_width(self):
        col_width = [len(h) for h in self.table_header]
        for row in self.table_data:
            for i, col in zip(range(len(row)), row):
                if len(col) > col_width[i]:
                    col_width[i] = len(col)
        return col_width

    @property
    def rst_table(self):
        separator = '+'
        for w in self.columns_width:
            separator += '-' * (w + 2) + '+'
        t = []
        t.append(separator)
        r = '|'
        for i, c in zip(range(len(self.table_header)), self.table_header):
            r += ' ' + c + ' ' * (self.columns_width[i] + 2 - len(c) - 1) + '|'
        t.append(r)
        t.append(separator)

        for row in self.table_data:
            r = '|'
            for i, c in zip(range(len(row)), row):
                r += ' ' + c + ' ' * (self.columns_width[i] + 2 - len(c) - 1) + '|'
            t.append(r)
            t.append(separator)
        return '\n'.join(t)
