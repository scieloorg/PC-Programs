# coding = utf-8

import sys

from modules import xmlcvrter as xmlcvrter


#path, acron = xmlpkgmker.validated_packages(sys.argv, 'j1.0')

#xmlcvrter.convert(['convert', path, acron])

xmlcvrter.convert(sys.argv)
