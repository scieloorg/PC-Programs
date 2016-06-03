error = []
children = {}
parents = {}
tag = ''
for line in open('../src/scielo/bin/markup_xml/app_core/tree.txt', 'r').readlines():
    line = line.strip()
    if ';' in line:
        parts = line.split(';')
        child_name = parts[0]
        children[tag].append(child_name)
        if not child_name in parents.keys():
            parents[child_name] = []
        parents[child_name].append(tag)
    else:
        if len(line) > 0:
            tag = line
            children[tag] = []


def links(a_list, address=''):
    if isinstance(a_list, list):
        a = ['`' + item + '`_' for item in sorted(a_list)]
        return ', '.join(a)
    else:
        return ''


def links_to_attr(a_list, address=''):
    a = ['`' + item + ' <markup_tags.html#attribute-' + item.replace(' ', '-') + '>`_' for item in a_list]
    return ', '.join(a)


def links_other_page(a_list, other_page):
    a = ['`' + item + ' <' + other_page + '#' + item.replace(' ', '-') + '>`_' for item in a_list]
    return ', '.join(a)


def element(definition, children, parents, attributes, tag):
    print(tag)
    print('-'*len(tag))
    print('\nElement')
    print('\n' + definition)
    if parents.get(tag) is not None:
        if len(parents[tag]) > 0:
            print('\nContained in: ' + links(parents.get(tag)))

    if children.get(tag) is not None:
        if len(children[tag]) > 0:
            print('\nContains: ' + links(children.get(tag)))

    if tag in attributes.keys():
        print('\nAttributes: ' + links_to_attr(attributes[tag]))
    else:
        print('\nAttributes: none')
    print('')


def auto_element(definition, children, parents, attributes, tag):
    print(tag)
    print('-'*len(tag))
    print('\nAutomatic identification of `' + tag[1:] + '`_')
    print('\n' + definition)
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

    if c > 0:
        i = 0
        print('\n\n+' + '-'*c + '+' + '-'*v + '+')
        for code in attribute_codes:
            value = attribute_values[i]
            n_c = c - len(code)
            n_v = v - len(value)

            print('|' + code + ' '*n_c + '|' + value + ' '*n_v + '|')
            print('+' + '-'*c + '+' + '-'*v + '+')
            i += 1
    print('\n')


def print_attribute(attributes_data, attribute_in, attribute_name):
    print('Attribute ' + attribute_name)
    print('-'*len('Attribute ' + attribute_name))
    print('\nAttribute')
    print('\n' + attributes_data[attribute_name][0])
    print('\nIs attribute of: ' + links(attribute_in[attribute_name]))
    print_attribute_values(attributes_data[attribute_name][1], attributes_data[attribute_name][2])
    print('\n')


f = open('attributes_data.txt', 'r')
attributes_data_content = f.readlines()
f.close()

f = open('attributes_def.txt', 'r')
attributes_def_content = f.readlines()
f.close()

attribute_in = {}
attributes_list = {}
for item in attributes_def_content:
    k, v = item.strip().split('|')
    attributes_list[k] = []
    attributes_list[k].append(v)
    attribute_in[k] = []

for item in attributes_data_content:
    item = item.strip()
    if item.startswith('sec-type'):
        k, values, codes = item.split('#')
    else:
        k, values, codes = item.split('|')
    attributes_list[k].append(values.split(';'))
    attributes_list[k].append(codes.split(';'))


tag = ''
i = 0
tag_attributes = {}
for item in open('../src/scielo/bin/markup_xml/app_core/link.mds', 'r').readlines():
    item = item.strip()
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

definitions = {}
for item in open('../src/scielo/bin/markup_xml/app_core/tree_en.txt', 'r').readlines():
    i = item.strip()
    k, v = i.split(';')
    definitions[k] = v

title = 'SciELO Markup Elements and Attributes'
print('='*len(title))
print(title)
print('='*len(title))


print('Automations')
print('===========')

for item in sorted(children.keys()):
    if '*' in item:
        auto_element(definitions.get(item, ''), children, parents, tag_attributes, item)

print('Elements')
print('========')

for item in sorted(children.keys()):
    if not '*' in item:
        element(definitions.get(item, ''), children, parents, tag_attributes, item)

print('Attributes')
print('==========')
for item in sorted(attributes_list.keys()):
    print_attribute(attributes_list, attribute_in, item)
print(error)
