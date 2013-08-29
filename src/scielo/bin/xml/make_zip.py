import os
import sys
import zipfile

xmls = [f.replace('.xml', '') for f in os.listdir(sys.argv[1]) if f.endswith('.xml')]
d = sys.argv[1] + '_zips'
os.makedirs(d)
for x in xmls:
    zipf = zipfile.ZipFile(d + '/' + x + '.zip', 'w')
    for f in os.listdir(sys.argv[1]):
        if f.startswith(x):
            zipf.write(sys.argv[1] + '/' + f)
    zipf.close()
