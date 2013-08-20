import sys
import os

version = '3.0'
sys.argv = [arg.replace('\\', '/') for arg in sys.argv]
script_name = sys.argv[0]

if len(sys.argv) == 3:
    ign, src, acron = sys.argv
    if (os.path.isfile(src) and src.endswith('.xml')) or (os.path.isdir(src) and [f for f in os.listdir(src) if f.endswith('.xml')]):
        import xmlpkgmker
        xmlpkgmker.make_packages(src, acron, version)
    else:
        print(src + ' is not a folder neither a XML file')
elif len(sys.argv) == 2:
    ign, src = sys.argv
    if src.endswith('.sgm.xml'):
        import xmlpkgmker
        xmlpkgmker.make_packages(src, '', version)
else:
    print('Usage:')
    print('python ' + script_name + ' <src> <acron>')
    print('where <src> = xml filename or path where there are xml files')
