import os
import sys
import zipfile

pdfs = [f.replace('.pdf', '') for f in os.listdir(sys.argv[1]) if f.endswith('.pdf')]
xmls = [f for f in os.listdir(sys.argv[1]) if f.endswith('.xml')]
other = [f for f in os.listdir(sys.argv[1]) if not f.endswith('.xml') and not f.endswith('.pdf')]

d = sys.argv[1] + '_zips'
os.makedirs(d)

for pdf in pdfs:
    for xml in xmls:
        if xml.startswith(pdf):
            zipf = zipfile.ZipFile(d + '/' + xml.replace('.xml', '') + '.zip', 'w')
            zipf.write(sys.argv[1] + '/' + xml, arcname = xml)
            zipf.write(sys.argv[1] + '/' + pdf + '.pdf', arcname = pdf + '.pdf')
            for o in other:
                if o.startswith(pdf):
                    zipf.write(sys.argv[1] + '/' + o, arcname = o)
            zipf.close()
