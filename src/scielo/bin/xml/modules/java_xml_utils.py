# coding=utf-8
import sys
import os
import shutil
import tempfile

import xml_utils
import fs_utils


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))
JAVA_PATH = 'java'
JAR_TRANSFORM = THIS_LOCATION + '/../../jar/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = THIS_LOCATION + '/../../jar/XMLCheck.jar'
TMP_DIR = THIS_LOCATION + '/../../tmp'


if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)


def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if v != '':
            if ' ' in v:
                r += k + '=' + '"' + v + '" '
            else:
                r += k + '=' + v + ' '
    return r


class XML(object):

    def __init__(self, xml, doctype=None):
        self.xml_filename = xml if not '<' in xml else None
        self.content = xml if '<' in xml else fs_utils.read_file(xml)
        self.doctype = doctype
        if doctype is not None:
            self._backup_xml_file()
            self._change_doctype()

    def _backup_xml_file(self):
        self.backup_path = tempfile.mkdtemp()
        self.backup_xml_filename = self.backup_path + '/' + os.path.basename(self.xml_filename)
        shutil.copyfile(self.xml_filename, self.backup_xml_filename)

    def finish(self):
        if self.doctype is not None:
            shutil.move(self.backup_xml_filename, self.xml_filename)
            try:
                shutil.rmtree(self.backup_path)
            except:
                pass

    def _change_doctype(self):
        self.content = self.content.replace('\r\n', '\n')
        if '<!DOCTYPE' in self.content:
            find_text = self.content[self.content.find('<!DOCTYPE'):]
            find_text = find_text[0:find_text.find('>')+1]
            if len(find_text) > 0:
                if len(self.doctype) > 0:
                    self.content = self.content.replace(find_text, self.doctype)
                else:
                    if find_text + '\n' in self.content:
                        self.content = self.content.replace(find_text + '\n', self.doctype)
        elif self.content.startswith('<?xml '):
            if '?>' in self.content:
                xml_proc = self.content[0:self.content.find('?>')+2]
            xml = self.content[1:]
            if '<' in xml:
                xml = xml[xml.find('<'):]
            if len(self.doctype) > 0:
                self.content = xml_proc + '\n' + self.doctype + '\n' + xml
            else:
                self.content = xml_proc + '\n' + xml
        fs_utils.write_file(self.xml_filename, self.content)

    def transform_content(self, xsl_filename):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.close()

        f2 = tempfile.NamedTemporaryFile(delete=False)
        f2.close()

        fs_utils.write_file(f.name, self.content)

        content = ''
        if self.transform_file(f.name, xsl_filename, f2.name):
            content = fs_utils.read_file(f2.name)

        for item in [f.name, f2.name]:
            os.unlink(f.name)
        return content

    def prepare(self, result_filename):
        temp_result_filename = TMP_DIR + '/' + os.path.basename(result_filename)
        result_path = os.path.dirname(result_filename)
        if not os.path.isdir(result_path):
            os.makedirs(result_path)
        for f in [result_filename, temp_result_filename]:
            if os.path.isfile(f):
                os.unlink(f)
        return temp_result_filename

    def transform_file(self, xsl_filename, result_filename, parameters={}):
        error = False

        temp_result_filename = self.prepare(result_filename)

        cmd = JAVA_PATH + ' -jar "' + JAR_TRANSFORM + '" -novw -w0 -o "' + temp_result_filename + '" "' + self.xml_filename + '" "' + xsl_filename + '" ' + format_parameters(parameters)
        cmd = cmd.encode(encoding=sys.getfilesystemencoding())
        os.system(cmd)

        if not os.path.exists(temp_result_filename):
            fs_utils.write_file(temp_result_filename, 'ERROR: transformation error.\n' + cmd)
            error = True
        shutil.move(temp_result_filename, result_filename)

        return (not error)

    def xml_validate(self, result_filename):
        validation_type = '' if self.doctype == '' else '--validate'
        temp_result_filename = self.prepare(result_filename)

        cmd = JAVA_PATH + ' -cp "' + JAR_VALIDATE + '" br.bireme.XMLCheck.XMLCheck "' + self.xml_filename + '" ' + validation_type + '>"' + temp_result_filename + '"'
        cmd = cmd.encode(encoding=sys.getfilesystemencoding())
        os.system(cmd)

        if os.path.exists(temp_result_filename):
            result = fs_utils.read_file(temp_result_filename, sys.getfilesystemencoding())
            if 'ERROR' in result.upper():
                n = 0
                s = ''
                for line in open(self.xml_filename, 'r').readlines():
                    if n > 0:
                        s += str(n) + ':' + line
                    n += 1
                result += '\n' + s.decode('utf-8')
                fs_utils.write_file(temp_result_filename, result)
        else:
            result = 'ERROR: Not valid. Unknown error.\n' + cmd
            fs_utils.write_file(temp_result_filename, result)

        shutil.move(temp_result_filename, result_filename)
        return not 'ERROR' in result.upper()


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
    #register_log('xml_transform: inicio')
    error = False

    temp_result_filename = TMP_DIR + '/' + os.path.basename(result_filename)

    if not os.path.isdir(os.path.dirname(result_filename)):
        os.makedirs(os.path.dirname(result_filename))
    for f in [result_filename, temp_result_filename]:
        if os.path.isfile(f):
            os.unlink(f)
    tmp_xml_filename = create_temp_xml_filename(xml_filename)
    cmd = JAVA_PATH + ' -jar "' + JAR_TRANSFORM + '" -novw -w0 -o "' + temp_result_filename + '" "' + tmp_xml_filename + '" "' + xsl_filename + '" ' + format_parameters(parameters)
    cmd = cmd.encode(encoding=sys.getfilesystemencoding())
    os.system(cmd)
    if not os.path.exists(temp_result_filename):
        fs_utils.write_file(temp_result_filename, 'ERROR: transformation error.\n' + cmd)
        error = True
    shutil.move(temp_result_filename, result_filename)

    fs_utils.delete_file_or_folder(tmp_xml_filename)
    #register_log('xml_transform: fim')

    return (not error)


def xml_validate(xml_filename, result_filename, doctype=None):
    #register_log('xml_validate: inicio')
    validation_type = ''

    if doctype is None:
        doctype = ''
    else:
        validation_type = '--validate'

    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    temp_result_filename = TMP_DIR + '/' + os.path.basename(result_filename)
    if os.path.isfile(result_filename):
        os.unlink(result_filename)
    if not os.path.isdir(os.path.dirname(result_filename)):
        os.makedirs(os.path.dirname(result_filename))

    cmd = JAVA_PATH + ' -cp "' + JAR_VALIDATE + '" br.bireme.XMLCheck.XMLCheck "' + xml_filename + '" ' + validation_type + '>"' + temp_result_filename + '"'
    cmd = cmd.encode(encoding=sys.getfilesystemencoding())
    os.system(cmd)

    if os.path.exists(temp_result_filename):
        result = fs_utils.read_file(temp_result_filename, sys.getfilesystemencoding())

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
    #register_log('xml_validate: fim')
    return not 'ERROR' in result.upper()


def create_temp_xml_filename(xml_filename):
    tmp_filename = TMP_DIR + '/' + os.path.basename(xml_filename)
    shutil.copyfile(xml_filename, tmp_filename)
    return tmp_filename
