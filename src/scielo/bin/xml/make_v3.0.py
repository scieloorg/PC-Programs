import sys
import xmlpkgmker

xmlpkgmker.DEBUG = 'ON'
xmlpkgmker.call_make_packages(sys.argv, '3.0')
