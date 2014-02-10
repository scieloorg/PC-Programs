f = open('../src/scielo/bin/markup_xml/app_core/attb.mds', 'r')
definitions = f.readlines()
f.close()
f = open('../src/scielo/bin/markup_xml/en_attb.mds', 'r')
definitions += f.readlines()
f.close()

f = open('attributes_data.txt', 'w')
f2 = open('attributes_def0.txt', 'w')

i = 0

for item in definitions:
    a = item.replace('\n', '').replace('\r', '')
    i += 1
    if i == 1:
        tag = a
    elif i == 2:
        if a == '':
            attr = ''
        else:
            attr = a
    elif i == 3:
        f.write(tag + '|' + attr + '|' + a + '\n')
        f2.write(tag + '|' + '\n')
    elif i == 4:
        i = 0
f.close()
f2.close()
