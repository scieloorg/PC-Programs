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


for k in sorted(translations.keys()):
    print(k + ';' + translations.get(k, '')) 