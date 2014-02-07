f = open('../src/scielo/bin/markup_xml/app_core/attb.mds', 'r')
definitions = f.readlines()
f.close()
f = open('../src/scielo/bin/markup_xml/en_attb.mds', 'r')
definitions += f.readlines()
f.close()


i = 0

for item in definitions:
    a = item.replace('\n', '').replace('\r', '')
    i += 1
    if i == 1:
        tag = a
    elif i == 2:
        if a == '':
            attr = 'no'
        else:
            attr = 'yes'
    elif i == 3:
        print(tag + '|' + attr + '|')
        i = 0
