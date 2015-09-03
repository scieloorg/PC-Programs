# coding=utf-8
import sys
import os
import shutil
import tempfile
from datetime import datetime


import xml_utils
import fs_utils


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))
JAVA_PATH = 'java'
JAR_TRANSFORM = THIS_LOCATION + '/../../jar/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = THIS_LOCATION + '/../../jar/XMLCheck.jar'


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if v != '':
            if ' ' in v:
                r += k + '=' + '"' + v + '" '
            else:
                r += k + '=' + v + ' '
    return r


def xml_content_transform(content, xsl_filename):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()

    fs_utils.write_file(f.name, content)

    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.close()
    if xml_transform(f.name, xsl_filename, f2.name):
        content = fs_utils.read_file(f2.name)
        os.unlink(f2.name)
    if os.path.exists(f.name):
        os.unlink(f.name)
    return content


def xml_transform(xml_filename, xsl_filename, result_filename, parameters={}):
    register_log('xml_transform: inicio')
    error = False

    tmp_dir = tempfile.mkdtemp()
    temp_result_filename = tmp_dir + '/' + os.path.basename(result_filename)

    if not os.path.isdir(os.path.dirname(result_filename)):
        os.makedirs(os.path.dirname(result_filename))
    for f in [result_filename, temp_result_filename]:
        if os.path.isfile(f):
            os.unlink(f)

    cmd = JAVA_PATH + ' -jar "' + JAR_TRANSFORM + '" -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)
    cmd = cmd.encode(encoding=sys.getfilesystemencoding())
    os.system(cmd)

    if not os.path.exists(temp_result_filename):
        fs_utils.write_file(temp_result_filename, 'ERROR: transformation error.\n' + cmd)
        error = True
    shutil.move(temp_result_filename, result_filename)

    if os.path.isdir(tmp_dir):
        try:
            shutil.rmtree(tmp_dir)
        except:
            pass
    register_log('xml_transform: fim')
    return (not error)


def xml_validate(xml_filename, result_filename, doctype=None):
    register_log('xml_validate: inicio')
    validation_type = ''

    if doctype is None:
        doctype = ''
    else:
        validation_type = '--validate'

    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    tmp_dir = tempfile.mkdtemp()
    temp_result_filename = tmp_dir + '/' + os.path.basename(result_filename)
    if os.path.isfile(result_filename):
        os.unlink(result_filename)
    if not os.path.isdir(os.path.dirname(result_filename)):
        os.makedirs(os.path.dirname(result_filename))

    cmd = JAVA_PATH + ' -cp "' + JAR_VALIDATE + '" br.bireme.XMLCheck.XMLCheck "' + xml_filename + '" ' + validation_type + '>"' + temp_result_filename + '"'
    cmd = cmd.encode(encoding=sys.getfilesystemencoding())
    os.system(cmd)

    if os.path.exists(temp_result_filename):
        result = fs_utils.read_file(temp_result_filename)

        if 'ERROR' in result.upper():
            n = 0
            s = ''
            for line in open(xml_filename, 'r').readlines():
                if n > 0:
                    s += str(n) + ':' + line
                n += 1
            result += '\n' + s.decode('utf-8')
            fs_utils.write_file(temp_result_filename, result)
    else:
        result = 'ERROR: Not valid. Unknown error.\n' + cmd
        fs_utils.write_file(temp_result_filename, result)

    shutil.move(temp_result_filename, result_filename)
    shutil.move(bkp_xml_filename, xml_filename)
    if os.path.isdir(tmp_dir):
        try:
            shutil.rmtree(tmp_dir)
        except:
            pass
    register_log('xml_validate: fim')
    return not 'ERROR' in result.upper()
