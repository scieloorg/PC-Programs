def clean_issn():
    files = ['issn.seq', 'issn_norm.seq']
    c = {}
    for f in files:
        fp = open('../inputs/' + f, 'r')
        c[f] = fp.readlines()
        fp.close()

    norm_titles = [ item.split('|')[1].upper() for item in c['issn_norm.seq'] ]
    

    cleaned = []
    f = open('../inputs/issn_cleaned.seq', 'w')
    for row in c['issn.seq']:
        if not row in c['issn_norm.seq']:
            title = row.split('|')[1].upper().replace('  ', ' ')
            chr_title = [ character for character in title if  character in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' ]
            new_title = ''.join(chr_title)
            if not new_title in norm_titles:
                if not new_title in cleaned:
                    cleaned.append(new_title)
                    f.write(new_title + '|' + row)
    f.close()

def normalize_title(t):
    title = t.upper().replace('  ', ' ')
    chr_title = [ character for character in title if  character in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' ]
    

    return  ''.join(chr_title)

def normalize_file():
    f = open('../inputs/issn.seq', 'r')	
    rows = f.readlines()
    f.close()
    f = open('../inputs/issn00.seq', 'w')
    normalized = []
    for row in rows:
    	d = row.split('|')
        norm = normalize_title(d[1])
        if not norm in normalized:
            normalized.append(norm)
            f.write(d[0] + '|' + norm + '\n')
    f.close()




normalize_file()

            