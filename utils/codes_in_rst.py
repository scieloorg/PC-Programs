# encoding = iso-8859-1
#mx code lw=999 "pft=if v1^l='en' or a(v1^l)  then (v1^*[1],'|',v1^l[1],'|',v2^c,'|',v2^v/) fi" now > code.txt

f = open('code.txt', 'r')
items = f.readlines()
f.close()


f = open('attributes_def.txt', 'r')
definitions = f.readlines()
f.close()

def_list = {}
for item in definitions:
    k, v = item.replace('\n', '').replace('\r', '').split('|')
    def_list[k] = v

f = open('attributes_data.txt', 'r')
attributes_data = f.readlines()
f.close()

attribute_data = {}
for item in attributes_data:
    attribute_data[k] = item.replace('\n', '').replace('\r', '').split('|')
    
dimension_code = {}
dimension_value = {}

d = {}
for i in items:
    try:
        name, lng, code, value = i.replace('\n', '').replace('\r', '').split('$')
        v = d.get(name, None)
        if v is None:
            d[name] = {}
            dimension_value[name] = 0
            dimension_code[name] = 0
        d[name][code] = value
        if len(code) > dimension_code[name]:
            dimension_code[name] = len(code)
        if len(value) > dimension_value[name]:
            dimension_value[name] = len(value)
    except:
        print i

for table_name, table_content in sorted(d.items()):
    print(table_name)
    print('='*len(table_name))
    print(def_list.get(table_name, '{missing description}'))
    print('+' + '-'*dimension_code[table_name] + '+' + '-'*dimension_value[table_name] + '+')
    for code, value in sorted(table_content.items()):
        n_c = dimension_code[table_name] - len(code)
        n_v = dimension_value[table_name] - len(value)

        print('|' + code + ' '*n_c + '|' + value + ' '*n_v + '|')
        print('+' + '-'*dimension_code[table_name] + '+' + '-'*dimension_value[table_name] + '+')
    print('')

