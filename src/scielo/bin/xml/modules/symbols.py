# coding=utf-8

import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
path = CURRENT_PATH + '/../tables'

symbols = None

#<td><font face="Symbol" size="+2">&#167;</font></td><td nowrap>&lt;font face=&quot;Symbol&quot;&gt;&amp;#167;&lt;/font&gt;</td><td>club</td><td>&amp;clubs; &nbsp;is&nbsp; <span class="b">&clubs;</span></td><td>&amp;#9827; &nbsp;is&nbsp; <span class="b">&#9827;</span></td><td>Black club suit</td><td>WGL4</td></tr>
#caracter|source html|name|...|...|def|?
# 0 | 4 | 5 
def html2table():
    _items = []
    c = open(path + '/symbols.html', 'r').read()
    if not isinstance(c, unicode):
        c = c.decode('utf-8')
    c = c.replace('<tr', '~BREAK~<tr').replace('</tr>', '</tr>~BREAK~')
    items = [item for item in c.split('~BREAK~') if item.startswith('<tr') and item.endswith('</tr>') and 'Symbol' in item]
    for item in items:
        item = item.replace('<td ', '<td>')
        cells = item.split('</td><td>')
        if len(cells) == 7:
            _char = cells[0]
            _ent = cells[4]
            _def = cells[5]
            _char = _char[0:_char.rfind('</font>')]
            _char = _char[_char.rfind('>')+1:]
            _ent = _ent[_ent.rfind('&'):]
            _ent = _ent[0:_ent.rfind(';')+1]
            _items.append(_char + '\t' + _ent + '\t' + _def)
    open(path + '/symbols.csv', 'w').write('\n'.join(_items).encode('utf-8'))


def load_symbols():
    symbols_items = {}
    for row in open(path + '/symbols.csv', 'r').readlines():
        if not isinstance(row, unicode):
            row = row.decode('utf-8')
        cells = row.split('\t')
        if len(cells) == 3:
            char, ent, descr = cells
            symbols_items[char] = ent
    return symbols_items


def get_symbol(c):
    global symbols
    if symbols is None:
        symbols = load_symbols()
    return symbols.get(c, '?')


if not os.path.isfile(CURRENT_PATH + '/../tables/symbols.csv'):
    html2table()
if os.path.isfile(CURRENT_PATH + '/../tables/symbols.csv'):
    if symbols is None:
        symbols = load_symbols()

