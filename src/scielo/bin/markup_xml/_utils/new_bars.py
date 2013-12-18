f = open('../app_core/en_bars.tr')
content = f.readlines()
f.close()
translations = {}
for row in content:
    cols = row.replace('\r', '').replace('\n', '').split(';')
    if len(cols) == 2:
        term = cols[1]
        
    elif len(cols) == 1:
        if len(cols[0]) > 0:
            translations[term] = cols[0]


f = open('../app_core/pt_bars.mds')
content = f.readlines()
f.close()

tag_and_bar = {}

tree = {}
definition = {}
barname = ''
for row in content:
    row = row.replace('\r', '').replace('\n', '')
    cols = row.split(';')
    if len(cols) == 6:
        tag_and_bar[cols[0]] = cols[5]
        definition[cols[0]] = translations.get(cols[0], 'Identify the ' + cols[0])
        tree[barname].append((cols[0], cols[3]))
    elif len(cols) == 2:
        if not cols[0] == 'down':
            if not cols[0] in tree:
                tree[cols[0]] = []
            barname = cols[0]

for key in sorted(definition.keys()):
    print(key)
    barname = tag_and_bar.get(key, None)
    if barname is not None:
        for child in tree.get(barname, []):
            print(child[0] + ';' + child[1])
    print('')
