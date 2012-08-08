
def get_char(line, t):
    c = ''
    if t in line:
        c = line[line.find(t)+len(t):]
        c = c[0:c.find(',')]
    return c

f=open('table_ent','r')
c=f.readlines()
f.close()
type = ['small ', 'capital ']
for line in c:
    for t in type:
        new = get_char(line, t)
        if not new == '':
            line = line.replace("\n", '|' + new )

    print(line)
