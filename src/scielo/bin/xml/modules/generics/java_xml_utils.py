# coding=utf-8
import sys
import os
import shutil

from . import xml_utils
from . import fs_utils
from . import system

from ..__init__ import JAR_PATH
from ..__init__ import TMP_DIR


JAVA_PATH = 'java'
JAR_TRANSFORM = JAR_PATH + '/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = JAR_PATH + '/XMLCheck.jar'


if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)


def format_parameters(parameters):
    return ' '.join(['{}="{}"'.format(k, v) for k, v in parameters.items()])


class XMLValidator(object):

    def __init__(self, xml_filename, result_filename, doctype=None):
        self.xml_filename = xml_filename
        self.result_filename = result_filename
        self.doctype = doctype

    def _setup(self):
        self.temp_result_filename = TMP_DIR + '/' + os.path.basename(self.result_filename)
        self.temp_result_dir = os.path.dirname(self.result_filename)
        self.validation_type = '' if self.doctype is None else '--validate'

        self.bkp = fs_utils.read_file(self.xml_filename)
        xml_utils.new_apply_dtd(self.xml_filename, self.doctype)

        fs_utils.delete_file_or_folder(self.result_filename)
        fs_utils.delete_file_or_folder(self.temp_result_filename)
        if not os.path.isdir(self.temp_result_dir):
            os.makedirs(self.temp_result_dir)

    @property
    def _command(self):
        return u'java -cp "{}" br.bireme.XMLCheck.XMLCheck "{}" {}>"{}"'.format(
            JAR_VALIDATE,
            self.xml_filename,
            self.validation_type,
            self.temp_result_filename)

    def _is_valid(self):
        result = ''
        if os.path.exists(self.temp_result_filename):
            encoding = sys.getfilesystemencoding()
            print(encoding)
            result = fs_utils.read_file(self.temp_result_filename, encoding)

            if 'ERROR' in result.upper():
                lines = fs_utils.read_file_lines(self.xml_filename, encoding)[1:]
                numbers = [str(i) + ':' for i in range(1, len(lines)+1)]
                lines = '\n'.join([n + line for n, line in zip(numbers, lines)])
                fs_utils.write_file(self.temp_result_filename, result + lines, encoding)
        else:
            result = 'ERROR: Not valid. Unknown error.\n' + self._command
            fs_utils.write_file(self.temp_result_filename, result)
        return 'ERROR' not in result.upper()

    def xml_validate(self):
        self._setup()
        cmd = self._command
        system.run_command(cmd)
        valid = self._is_valid()
        shutil.move(self.temp_result_filename, self.result_filename)
        fs_utils.write_file(self.xml_filename, self.bkp)
        return valid


class XMLTransformer(object):

    def __init__(self, xml_filename, xsl_filename, result_filename, parameters={}):
        self.xml_filename = xml_filename
        self.result_filename = result_filename
        self.xsl_filename = xsl_filename
        self.parameters = parameters

    def _setup(self):
        self.temp_result_filename = TMP_DIR + '/' + os.path.basename(self.result_filename)
        self.temp_result_dir = os.path.dirname(self.result_filename)

        self.bkp = fs_utils.read_file(self.xml_filename)
        xml_utils.new_apply_dtd(self.xml_filename, '')
        fs_utils.delete_file_or_folder(self.result_filename)
        fs_utils.delete_file_or_folder(self.temp_result_filename)
        if not os.path.isdir(self.temp_result_dir):
            os.makedirs(self.temp_result_dir)

    @property
    def _command(self):
        return JAVA_PATH + ' -jar "' + JAR_TRANSFORM + '" -novw -w0 -o "' + self.temp_result_filename + '" "' + self.xml_filename + '" "' + self.xsl_filename + '" ' + format_parameters(self.parameters)

    def xml_transform(self):
        self._setup()
        cmd = self._command
        system.run_command(cmd)
        error = False
        if not os.path.exists(self.temp_result_filename):
            fs_utils.write_file(self.temp_result_filename, 'ERROR: transformation error.\n' + cmd)
            error = True
        shutil.move(self.temp_result_filename, self.result_filename)
        fs_utils.write_file(self.xml_filename, self.bkp)
        return (not error)


def xml_transform(xml, xsl, result, parameters={}):
    if xml != result:
        return XMLTransformer(xml, xsl, result, parameters).xml_transform()
    return 'xml_transform: xml {} must be different from result {}'.format(xml, result)


def xml_validate(xml_filename, report_filename, doctype):
    return XMLValidator(xml_filename, report_filename, doctype).xml_validate()


def xml_content_transform(content, xsl_filename):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()
    fs_utils.write_file(f.name, content)

    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.close()

    XMLTransformer(f.name, xsl_filename, f2.name).xml_transform()
    content = fs_utils.read_file(f2.name)

    fs_utils.delete_file_or_folder(f2.name)
    fs_utils.delete_file_or_folder(f.name)
    return content
