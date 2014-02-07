error = []


def links(a_list):
    a = ['`' + item + '`_' for item in a_list]
    return ', '.join(a)


def links_other_page(a_list, other_page):
    a = ['`' + item + ' <' + other_page + '#' + item.replace(' ', '-') + '>`_' for item in a_list]
    return ', '.join(a)


def navigate(tree, definition, contains, attributes, tag):
    children = ''
    print('')
    print(tag)
    print('-'*len(tag))
    print(definition[tag])
    print('Contained in: ' + links(contains[tag]))

    if tag in tree:
        if len(tree[tag]) > 0:
            children = 'Contains:'
            sep = ' '
            for item in tree[tag]:
                children += sep + '`' + item[0] + '`_'
                sep = ', '
            print(children)
    else:
        error.append(tag)
    print('Attributes: ' + links_other_page(attributes[tag], 'code_database.html'))


f = open('../src/scielo/bin/markup_xml/app_core/tree.txt', 'r')
lines = f.readlines()
f.close()

f = open('../src/scielo/bin/markup_xml/app_core/tree_en.txt', 'r')
translations = f.readlines()
f.close()

f = open('../src/scielo/bin/markup_xml/app_core/links.mds', 'r')
attributes = f.readlines()
f.close()


tag = ''
i = 0
attr_list = {}
for item in attributes:
    i += 1
    if i == 1:
        tag = item
    elif i == 2:
        attr_list[tag] = item.replace('\n', '').replace('\r', '').split(';')
    elif i == 3:
        i = 0

trans = {}
for item in translations:
    i = item.replace('\n', '').replace('\r', '')
    k, v = i.split(';')
    trans[k] = v

contains = {}
d = {}
for item in lines:
    i = item.replace('\n', '').replace('\r', '')
    if i != '':
        parts = i.split(';')
        if len(parts) == 1:
            d[i] = []
            key = i

        elif len(parts) == 2:
            d[key].append(parts)
            if not parts[0] in contains.keys():
                contains[parts[0]] = []
            contains[parts[0]].append(key)

for item in sorted(trans.keys()):
    navigate(d, trans, contains, attr_list, item)


print(error)
