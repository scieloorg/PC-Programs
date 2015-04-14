# coding=utf-8
import os
import sys
import zipfile

pdfs = [f for f in os.listdir(sys.argv[1]) if f.endswith('.pdf')]
xmls = [f for f in os.listdir(sys.argv[1]) if f.endswith('.xml')]
other = [f for f in os.listdir(sys.argv[1]) if not f.endswith('.xml') and not f.endswith('.pdf')]

d = sys.argv[1] + '_zips'
os.makedirs(d)

for xml in xmls:
    name = xml[0:-4]
    zipf = zipfile.ZipFile(d + '/' + name + '.zip', 'w')
    zipf.write(sys.argv[1] + '/' + xml, arcname=xml)
    for pdf in pdfs:
        if (name + '-') in pdf or (name + '.') in pdf:
            zipf.write(sys.argv[1] + '/' + pdf, arcname=pdf)
    for o in other:
        if o.startswith(name + '.') or o.startswith(name + '-'):
            zipf.write(sys.argv[1] + '/' + o, arcname=o)
    zipf.close()
