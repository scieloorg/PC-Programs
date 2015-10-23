# coding=utf-8

import shutil
import sys
import os

from modules import java_xml_utils


#required_parameters = ['', 'xml filename', 'xsl filename', 'result filename', 'ctrl filename', 'err filename' ]


sys.argv = [arg.replace('\\', '/') for arg in sys.argv]
script, xml_filename, xsl_filename, result_filename, ctrl_filename, err_filename = sys.argv

if os.path.exists(ctrl_filename):
    os.unlink(ctrl_filename)
if os.path.exists(err_filename):
    os.unlink(err_filename)

if not java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename):
    shutil.copyfile(result_filename, err_filename)
f = open(ctrl_filename, 'w')
f.write('done')
f.close()
