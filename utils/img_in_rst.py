f = open('img_in_rst.txt', 'r')
items = f.readlines()
f.close()

for item in items:
    img = item[item.find('image:: img/')+len('image:: img/'):]
    img = img.replace('\n','').replace('\r', '')
    print('mv en/' + img + ' .')

