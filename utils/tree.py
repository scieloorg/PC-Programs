error = []


def links(a_list, address=''):
    a = ['`' + item + '`_' for item in a_list]
    return ', '.join(a)


def links_to_attr(a_list, address=''):
    a = ['`' + item + ' <attribute-' + item.replace(' ', '-') + '>`_' for item in a_list]
    return ', '.join(a)


def links_other_page(a_list, other_page):
    a = ['`' + item + ' <' + other_page + '#' + item.replace(' ', '-') + '>`_' for item in a_list]
    return ', '.join(a)


def navigate(tree, definition, contains, attributes, tag):
    children = ''
    print('----')
    print(tag)
    print('-'*len(tag))
    print('Element')
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
    if tag in attributes.keys():
        print('Attributes: ' + links(attributes[tag]))
    else:
        print('Attributes: none')
    print('')


def print_attribute_values(attribute_values, attribute_codes):
    v = 0
    for item in attribute_values:
        if len(item) > v:
            v = len(item)
    c = 0
    for item in attribute_codes:
        if len(item) > c:
            c = len(item)

    i = 0
    print('+' + '-'*c + '+' + '-'*v + '+')
    for code in attribute_codes:
        value = attribute_values[i]
        n_c = c - len(code)
        n_v = v - len(value)

        print('|' + code + ' '*n_c + '|' + value + ' '*n_v + '|')
        print('+' + '-'*c + '+' + '-'*v + '+')
        i += 1
    print('')


def print_attribute(attributes_data, attribute_in, attribute_name):
    print('----')
    print('Attribute ' + attribute_name)
    print('-'*len('Attribute ' + attribute_name))
    print('Attribute')
    print(attributes_data[attribute_name][0])
    print('Is attribute of: ' + links(attribute_in[attribute_name]))
    print_attribute_values(attributes_data[attribute_name][1], attributes_data[attribute_name][2])
    print('')

f = open('../src/scielo/bin/markup_xml/app_core/tree.txt', 'r')
lines = f.readlines()
f.close()

f = open('../src/scielo/bin/markup_xml/app_core/tree_en.txt', 'r')
translations = f.readlines()
f.close()

f = open('../src/scielo/bin/markup_xml/app_core/link.mds', 'r')
tags_with_attrib = f.readlines()
f.close()

f = open('attributes_data.txt', 'r')
attributes_data_content = f.readlines()
f.close()

f = open('attributes_def.txt', 'r')
attributes_def_content = f.readlines()
f.close()

attribute_in = {}
attributes_list = {}
for item in attributes_def_content:
    k, v = item.replace('\n', '').replace('\r', '').split('|')
    attributes_list[k] = []
    attributes_list[k].append(v)
    attribute_in[k] = []

for item in attributes_data_content:
    item = item.replace('\n', '').replace('\r', '')
    if item.startswith('sec-type'):
        k, values, codes = item.split('#')
    else:
        k, values, codes = item.split('|')
    attributes_list[k].append(values.split(';'))
    attributes_list[k].append(codes.split(';'))


tag = ''
i = 0
tag_attributes = {}
for item in tags_with_attrib:
    item = item.replace('\n', '').replace('\r', '')
    i += 1
    if i == 1:
        tag = item
    elif i == 2:
        tag_attributes[tag] = item.split(';')
        for attr in tag_attributes[tag]:
            if not attr in attribute_in.keys():
                attribute_in[attr] = []
            attribute_in[attr].append(tag)
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
    navigate(d, trans, contains, tag_attributes, item)

for item in sorted(attributes_list.keys()):
    print_attribute(attributes_list, attribute_in, item)
print(error)
