import random
import os
import sys
import shutil
import tempfile
import xml.etree.ElementTree as etree
from StringIO import StringIO


try:
    import Image
    IMG_CONVERTER = True
except:
    IMG_CONVERTER = False

#from datetime import datetime

DEBUG = 'OFF'
# global variables
THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))

CONFIG_JAVA_PATH = 'java'
CONFIG_JAR_PATH = THIS_LOCATION + '/../jar'
CONFIG_ENT_TABLE_PATH = THIS_LOCATION
CONFIG_VERSIONS_PATH = THIS_LOCATION + '/../pmc'


JAVA_PATH = CONFIG_JAVA_PATH
JAR_TRANSFORM = CONFIG_JAR_PATH + '/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = CONFIG_JAR_PATH + '/XMLCheck.jar'
ENTITIES_TABLE_FILENAME = CONFIG_ENT_TABLE_PATH + '/entities2char'


def configure_versions_location():
    PMC_PATH = CONFIG_VERSIONS_PATH
    version_configuration = {}
    version_configuration['3.0'] = {}
    version_configuration['3.0']['sgm2xml'] = PMC_PATH + '/v3.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['3.0']['scielo'] = {}
    version_configuration['3.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['scielo']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['scielo']['css'] = PMC_PATH + '/v3.0/xsl/web/plus'
    version_configuration['3.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['3.0']['scielo']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['scielo']['xsl_preview'] = PMC_PATH + '/v3.0/xsl/previewers/scielo-html-novo.xsl'
    version_configuration['3.0']['scielo']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['3.0']['pmc'] = {}
    version_configuration['3.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['pmc']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['pmc']['css'] = PMC_PATH + '/v3.0/xsl/jpub/jpub-preview.css'
    version_configuration['3.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
    version_configuration['3.0']['pmc']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['pmc']['xsl_preview'] = [PMC_PATH + '/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
    #version_configuration['3.0']['pmc']['xsl_preview'] = None
    version_configuration['3.0']['pmc']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/pmc.xsl'

    version_configuration['j1.0'] = {}
    version_configuration['j1.0']['sgm2xml'] = PMC_PATH + '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['j1.0']['scielo'] = {}
    version_configuration['j1.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'

    version_configuration['j1.0']['scielo']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['scielo']['css'] = version_configuration['3.0']['scielo']['css']
    version_configuration['j1.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['j1.0']['scielo']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['scielo']['xsl_preview'] = version_configuration['3.0']['scielo']['xsl_preview']
    version_configuration['j1.0']['scielo']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['j1.0']['pmc'] = {}
    version_configuration['j1.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
    version_configuration['j1.0']['pmc']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['pmc']['css'] = version_configuration['3.0']['pmc']['css']
    version_configuration['j1.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/nlm-stylechecker.xsl'
    version_configuration['j1.0']['pmc']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['pmc']['xsl_preview'] = [PMC_PATH + '/j1.0/xsl/jpub/citations-prep/jpub1-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
    #version_configuration['j1.0']['pmc']['xsl_preview'] = None
    version_configuration['j1.0']['pmc']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/pmc.xsl'
    return version_configuration


###
def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if v != '':
            if ' ' in v:
                r += k + '=' + '"' + v + '" '
            else:
                r += k + '=' + v + ' '
    return r


### ENTITIES
class EntitiesTable:
    def __init__(self, filename='entities'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.table_number2char = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values
                if number_ent == '&#124;':
                    char = '|'
                if named_ent in ['&gt;', '&lt;', '&amp;']:
                    char = named_ent
                    #entity_char = named_ent.replace('&','').replace(';','')
                self.table_number2char[number_ent] = char
                if '&#x' in number_ent:
                    hex_ent = number_ent[2:-1]
                    dec_ent = str(int('0' + hex_ent, 16))
                    self.table_number2char['&#' + dec_ent + ';'] = char
                elif '&#' in number_ent:
                    dec_ent = number_ent[2:-1]
                    hex_ent = hex(int(dec_ent))
                    self.table_number2char['&#' + hex_ent[hex_ent.find('x'):] + ';'] = char
                    self.table_number2char['&#x' + hex_ent[hex_ent.find('x')+1:].upper() + ';'] = char

                self.table_named2char[named_ent] = char

        f = open('ent_teste.txt', 'w')
        f.write('\n'.join(self.table_number2char.keys()))
        f.close()

    def is_valid_char(self, char):
        return (char != '' and not char in ['>', '<', '&'])

    def is_valid_named(self, named):
        return (named != '' and not named in ['&gt;', '&lt;', '&amp;'])

    def ent2chr(self, ent):
        r = self.table_number2char.get(ent, None)
        if r is None:
            r = self.table_named2char.get(ent, None)
        if r is None:
            r = ent
        return r


def convert_ent_to_char(content, entities_table=None):
    def prefix_ent(N=7):
        return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

    not_found_named = []
    not_found_number = []
    if '&' in content:
        PREFIX_ENT = prefix_ent()
        while PREFIX_ENT in content:
            PREFIX_ENT = prefix_ent()

        ALLOWED_ENTITIES = {'&gt;': PREFIX_ENT + 'gt;', '&lt;': PREFIX_ENT + 'lt;', '&amp;': PREFIX_ENT + 'amp;', }
        for ent, new_ent in ALLOWED_ENTITIES.items():
            content = content.replace(ent, new_ent)

        if '&' in content:
            import HTMLParser
            h = HTMLParser.HTMLParser()
            try:
                content = h.unescape(content).decode('utf-8')
            except:
                #print('Unable to use h.unescape')
                pass

        if '&' in content:
            if entities_table:
                while '&' in content:
                    ent = content[content.find('&'):]
                    ent = ent[0:ent.find(';')+1]

                    char = entities_table.ent2chr(ent)
                    if char == ent:
                        content = content.replace(ent, ent.replace('&', PREFIX_ENT))
                        if '&#' in ent:
                            not_found_number.append(ent)
                        else:
                            not_found_named.append(ent)
                    else:
                        content = content.replace(ent, char)

        if not_found_named:
            f = open('unknown_ent_named.txt', 'a+')
            f.write('\n'.join(not_found_named))
            f.close()
        if not_found_number:
            f = open('unknown_ent_number.txt', 'a+')
            f.write('\n'.join(not_found_number))
            f.close()
        content = content.replace(PREFIX_ENT, '&')

    return content


### IMAGES
def img_to_jpeg(image_filename, jpg_path, replace=False):
    r = True
    if image_filename.endswith('.tiff') or image_filename.endswith('.eps') or image_filename.endswith('.tif'):
        image_name = os.path.basename(image_filename)
        jpg_filename = jpg_path + '/' + image_name[0:image_name.rfind('.')] + '.jpg'

        if not os.path.exists(jpg_filename) or replace:
            try:
                im = Image.open(image_filename)
                im.thumbnail(im.size)
                im.save(jpg_filename, "JPEG")
            except Exception as inst:
                if DEBUG == 'ON':
                    print('Unable to convert ')
                    print(image_filename)
                    print('to')
                    print(jpg_filename)
                    print(inst)
                    print('')
        r = os.path.exists(jpg_filename)
    return r


def images_to_jpeg(img_path, jpg_path, replace=False):
    r = False
    failures = []
    files = [f for f in os.listdir(img_path) if f.endswith('.tiff') or f.endswith('.eps') or f.endswith('.tif')]
    for f in files:
        #jpg_filename = jpg_path + '/' + f[0:f.rfind('.')] + '.jpg'
        image_filename = img_path + '/' + f
        if not img_to_jpeg(image_filename, jpg_path):
            failures.append(image_filename)

    converted = len(files)-len(failures)
    if converted != len(files):
        print('Converted ' + str(converted) + '/' + str(len(files)))
        print('Not converted')
        print('\n'.join(failures))
    r = len(files) == converted
    return r


### XML
def xml_validate(xml_filename, result_filename, dtd_validation=False):
    validation_type = ''

    if dtd_validation:
        validation_type = '--validate'

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)

    cmd = JAVA_PATH + ' -cp ' + JAR_VALIDATE + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' + validation_type + '>' + temp_result_filename
    #print(cmd)
    os.system(cmd)

    if os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'r')
        result_content = f.read().replace(xml_filename, os.path.basename(xml_filename))
        f.close()

        if 'ERROR' in result_content.upper():
            f = open(xml_filename, 'r')

            n = 0
            s = ''
            for line in f.readlines():
                if n > 0:
                    s += str(n) + ':' + line
                n += 1
            result_content += '\n' + s
    else:
        result_content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd

    if 'ERROR' in result_content.upper():
        f = open(temp_result_filename, 'w')
        f.write(result_content)
        f.close()
        valid = False
    else:
        valid = True

    shutil.move(temp_result_filename, result_filename)

    return valid


def xml_is_well_formed(content):
    if '<' in content:
        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            #print('xml_is_well_formed')
            print(e)
            r = None
    else:
        try:
            r = etree.parse(content)
        except Exception as e:
            #print('xml_is_well_formed')
            print(e)
            r = None
    return r


def xml_content_transform(content, xsl_filename):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()
    fp = open(f.name, 'w')
    fp.write(content)
    fp.close()
    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.close()
    if xml_transform(f.name, xsl_filename, f2.name):
        fp = open(f2.name, 'r')
        content = fp.read()
        fp.close()
        os.unlink(f2.name)
    if os.path.exists(f.name):
        os.unlink(f.name)
    return content


def xml_transform(xml_filename, xsl_filename, result_filename, parameters={}):
    error = False
    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)
    cmd = JAVA_PATH + ' -jar ' + JAR_TRANSFORM + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)
    os.system(cmd)
    #print(cmd)
    if not os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        error = True

    shutil.move(temp_result_filename, result_filename)

    return (not error)


def tranform_in_steps(xml_filename, xsl_list, result_filename, parameters={}, fix_dtd_location=''):
    input_filename = xml_filename + '.in'
    output_filename = xml_filename + '.out'
    error = False

    shutil.copyfile(xml_filename, input_filename)
    if os.path.exists(result_filename):
        os.unlink(result_filename)

    for xsl in xsl_list:
        r = xml_transform(input_filename, xsl, output_filename, parameters)
        if r:
            if fix_dtd_location:
                f = open(output_filename, 'r')
                c = f.read()
                f.close()
                find = '"' + os.path.basename(fix_dtd_location) + '"'
                if find in c:
                    c = c.replace(find, '"' + fix_dtd_location + '"')
                    f = open(output_filename, 'w')
                    f.write(c)
                    f.close()
            shutil.copyfile(output_filename, input_filename)
        else:
            error = True
            break

    if os.path.exists(input_filename):
        os.unlink(input_filename)
    shutil.move(output_filename, result_filename)
    return not error


###
class XMLFixer:

    def __init__(self):
        pass

    def fix_dtd_location(self, content, dtd_filename, doctype):
        if not dtd_filename in content:
            if not '<?xml ' in content:
                content = '<?xml version="1.0" encoding="utf-8"?>\n' + content

            if '<!DOCTYPE' in content:
                old_doctype = content[content.find('<!DOCTYPE'):]
                old_doctype = old_doctype[0:old_doctype.find('>')+1]
                content = content.replace(old_doctype, '')
            if not '<!DOCTYPE' in content:
                content = content.replace('\n<article ', doctype.replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')
        return content

    def fix(self, content):
        if not xml_is_well_formed(content):
            f = open('fix1.xml', 'w')
            f.write(content)
            f.close()
            content = self._fix_style_tags(content)
            if not xml_is_well_formed(content):
                f = open('fix2.xml', 'w')
                f.write(content)
                f.close()
                content = self._fix_open_close(content)
                if not xml_is_well_formed(content):
                    f = open('fix3.xml', 'w')
                    f.write(content)
                    f.close()
        return content

    def _fix_open_close(self, content):
        changes = []
        parts = content.split('>')
        for s in parts:
            if '<' in s:
                if not '</' in s and not '<!--' in s and not '<?' in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and not '=' in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            print(change)
            content = content.replace('<' + test + '>', '[' + test + ']')
        return content

    def _fix_style_tags(self, content):
        rcontent = content
        tags = ['italic', 'bold', 'sub', 'sup']
        tag_list = []
        for tag in tags:
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')
        if content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            content = self._fix_problem(tag_list, parts)
        return content

    def _fix_problem(self, tag_list, parts):
        expected_close_tags = []
        ign_list = []
        k = 0
        for part in parts:
            if part in tag_list:
                tag = part
                print('\ncurrent:' + tag)
                if tag.startswith('</'):
                    print('expected')
                    print(expected_close_tags)
                    print('ign_list')
                    print(ign_list)
                    if tag in ign_list:
                        print('remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:
                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)

                            if not matched:
                                print('not matched')

                                while not matched and len(expected_close_tags) > 0:

                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]

                                    matched = (expected_close_tags[-1] == tag)

                                print('...expected')
                                print(expected_close_tags)
                                print('...ign_list')
                                print(ign_list)

                            if matched:
                                del expected_close_tags[-1]
                else:
                    expected_close_tags.append(tag.replace('<', '</'))
            k += 1
        return ''.join(parts)


class ValidationFiles:
    def __init__(self, pkg_path, report_path, preview_path, suffix=''):
        self.pkg_path = pkg_path
        self.suffix = suffix
        self.report_path = report_path
        self.preview_path = preview_path
        if not os.path.exists(pkg_path):
            os.makedirs(pkg_path)
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        if preview_path:
            if not os.path.exists(preview_path):
                os.makedirs(preview_path)
        self.html_preview = None
        self.dtd_validation_report = None
        self.style_checker_report = None
        self.xml_output = None

    def name(self, curr_name, new_name):
        self.dtd_validation_report = self.report_path + '/' + curr_name + self.suffix + '.dtd.txt'
        self.style_checker_report = self.report_path + '/' + curr_name + self.suffix + '.rep.html'

        if self.preview_path == self.pkg_path:
            self.html_preview = self.preview_path + '/' + new_name + '.html'
        elif self.preview_path:
            self.html_preview = self.preview_path + '/' + curr_name + self.suffix + '.xml.html'
        else:
            self.html_preview = None

        self.xml_output = self.pkg_path + '/' + new_name + '.xml'


class XMLValidations:
    def __init__(self, pkg_name, default_version=None, entities_table=None):
        self.pkg_name = pkg_name
        self.entities_table = entities_table
        self.default_version = default_version
        if default_version:
            self.select_version(default_version)
        #dtd_filename, xsl_prep_report, xsl_report, xsl_preview, css_filename

    def select_version(self, dtd_version):
        self._selected_version = dtd_version
        if dtd_version == '1.0':
            self._selected_version = 'j1.0'
        version_data = _versions_.get(self._selected_version, {}).get(self.pkg_name)
        self.xsl_report = version_data.get('xsl_report', None)
        self.xsl_prep_report = version_data.get('xsl_prep_report', None)
        self.xsl_preview = version_data.get('xsl_preview', None)
        self.dtd_filename = version_data.get('dtd', None)
        self.css_filename = 'file:///' + version_data.get('css', None)
        self.xsl_output = version_data.get('xsl_output', None)
        self.doctype = version_data.get('doctype', None)
        self._report = []

    def log(self, content):
        print(content)

    def report(self, content):
        #print(content)
        self._report.append(content)

    def _style_checker_report(self, xml_filename, style_checker_report):
        # STYLE CHECKER REPORT
        report_ok = False
        xml_report = style_checker_report.replace('.html', '.xml')
        if os.path.exists(xml_report):
            os.unlink(xml_report)

        if xml_transform(xml_filename, self.xsl_prep_report, xml_report):
            # Generate self.report.html
            #self.log('transform ' + xml_report + ' ' + self.xsl_report + ' ' + style_checker_report)
            if os.path.exists(style_checker_report):
                os.unlink(style_checker_report)

            if xml_transform(xml_report, self.xsl_report, style_checker_report):
                os.unlink(xml_report)

                f = open(style_checker_report, 'r')
                c = f.read()
                f.close()

                report_ok = ('Total of errors = 0' in c)

                if report_ok:
                    self.report('Validation report. No errors found. Read ' + style_checker_report)
                else:
                    self.report('Validation report. Some errors were found. Read ' + style_checker_report)
            else:
                self.report('Unable to create validation report: ' + style_checker_report)
        else:
            self.report('Unable to generate xml for report: ' + xml_report)
        if DEBUG == 'ON':
            print('\n'.join(self._report))
        return report_ok

    def _preview(self, xml_filename, html_preview, xsl_param_img_path, xsl_param_new_name=''):
        preview_ok = False
        if os.path.exists(html_preview):
            os.unlink(html_preview)
        xsl_params = {'xml_article': xml_filename, 'path_img': xsl_param_img_path + '/', 'css':  self.css_filename, 'new_name': xsl_param_new_name}
        if type(self.xsl_preview) == type([]):
            preview_ok = tranform_in_steps(xml_filename, self.xsl_preview, html_preview, xsl_params, self.dtd_filename)
        else:
            #self.log('transform ' + xml_filename + ' ' + self.xsl_preview + ' ' + html_preview)
            preview_ok = xml_transform(xml_filename, self.xsl_preview, html_preview, xsl_params)
        if preview_ok:
            self.report('Preview ' + html_preview)
        else:
            self.report('Unable to create preview: ' + html_preview)
        return preview_ok

    def _output(self, xml_filename, xml_output):
        output_ok = False
        if os.path.exists(xml_output):
            os.unlink(xml_output)
        output_ok = xml_transform(xml_filename, self.xsl_output, xml_output)
        if output_ok:
            self.report('XML output ' + xml_output)
        else:
            self.report('Unable to create output: ' + xml_output)
        return output_ok

    def check_list(self, xml_filename, pkg_files, img_path, xsl_param_new_name=''):
        if DEBUG == 'ON':
            r = self._check_list(xml_filename, pkg_files, img_path, xsl_param_new_name)
        else:
            try:
                r = self._check_list(xml_filename, pkg_files, img_path, xsl_param_new_name)
            except Exception as inst:
                r = [False, False]
                print('\n===== ATTENTION =====\nThere was an unexpected error.\n Please, report it to roberta.takenaka@scielo.org or at https://github.com/scieloorg/PC-Programs/issues')
                print(inst)
        return r

    def _check_list(self, xml_filename, pkg_files, img_path, xsl_param_new_name=''):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)
        is_well_formed, is_dtd_valid, is_style_valid = [False, False, False]
        content = None
        xml = xml_is_well_formed(xml_filename)
        if not xml:
            print('Converting entities...')
            f = open(xml_filename, 'r')
            content = f.read()
            f.close()
            content = convert_ent_to_char(content, self.entities_table)
            xml = xml_is_well_formed(content)
            if xml:
                f = open(xml_filename, 'w')
                f.write(content)
                f.close()

        if xml:
            is_well_formed = True
            if self.default_version is None:
                dtd_version = xml.find('.').attrib.get('dtd-version', '1.0')
                self.select_version(dtd_version)
            #    print('Document version:' + dtd_version)
            #else:
            #    #print('Default version:' + self.default_version)
            temp_dir = tempfile.mkdtemp()
            temp_xml_filename = temp_dir + '/' + os.path.basename(xml_filename)
            shutil.copyfile(xml_filename, temp_xml_filename)

            if self.dtd_filename:
                if content is None:
                    f = open(xml_filename, 'r')
                    content = f.read()
                    f.close()
                content = XMLFixer().fix_dtd_location(content, self.dtd_filename, self.doctype)
                f = open(temp_xml_filename, 'w')
                f.write(content)
                f.close()

            if os.path.exists(temp_xml_filename):
                is_dtd_valid = xml_validate(temp_xml_filename, pkg_files.dtd_validation_report, True)

                # STYLE CHECKER REPORT
                is_style_valid = self._style_checker_report(temp_xml_filename, pkg_files.style_checker_report)

                # PREVIEW
                #if pkg_files.html_preview:
                #    self._preview(temp_xml_filename, pkg_files.html_preview, img_path, xsl_param_new_name)

                if pkg_files.xml_output:
                    self._output(temp_xml_filename, pkg_files.xml_output)
                os.unlink(temp_xml_filename)
                shutil.rmtree(temp_dir)

        #self.manage_output_files(xml_filename, pkg_files, is_well_formed, is_dtd_valid, is_style_valid)
        return [is_well_formed, is_dtd_valid, is_style_valid]


class XMLMetadata:
    def __init__(self, content):
        try:
            self.root = etree.parse(StringIO(content))
        except:
            self.root = None

    def _fix_issue_number(self, num, suppl=''):
        if num != '':
            if 'pr' in num:
                num = num.replace(' pr', '')
            else:
                parts = num.split()
                if len(parts) == 3:
                    num = parts[0]
                    suppl = parts[2]
                elif len(parts) == 2:
                    if 'sup' in parts[1].lower():
                        num, suppl = parts
                    elif 'sup' in parts[0].lower():
                        num = ''
                        suppl = parts[1]

        return [num, suppl]

    def _meta_xml(self, node):
        issn, volid, issueno, suppl, fpage, order = ['', '', '', '', '', '']
        issn = self.root.findtext('.//front/journal-meta/issn[1]')
        volid = node.findtext('./volume')
        issueno = node.findtext('./issue')
        suppl = node.findtext('./supplement')

        if not volid:
            volid = ''
        if not issueno:
            issueno = ''
        if not suppl:
            suppl = ''

        issueno, suppl = self._fix_issue_number(issueno, suppl)
        order = node.findtext('.//article-id[@pub-id-type="other"]')
        page = node.find('./fpage')
        if page.attrib.get('seq'):
            fpage = page.text + '-' + page.attrib.get('seq')
        else:
            fpage = page.text
        if not order:
            order = fpage
        return [issn, volid, issueno, suppl, fpage, order]

    def _metadata(self):
        issn, volid, issueno, suppl, fpage, order = ['', '', '', '', '', '']
        if self.root:

            node = self.root.find('.//article-meta')
            if node is not None:
                issn, volid, issueno, suppl, fpage, order = self._meta_xml(node)
            else:
                attribs = self.root.find('.').attrib
                issn = attribs.get('issn')
                volid = attribs.get('volid')
                issueno = attribs.get('issueno')
                supplvol = attribs.get('supplvol', '')
                supplno = attribs.get('supplno', '')
                suppl = supplno if supplno else supplvol
                fpage = attribs.get('fpage')
                order = attribs.get('order')
                if issueno == 'ahead':
                    issueno = '00'
                    volid = '00'
        return [issn, volid, issueno, suppl, fpage, order]

    def format_name(self, data, param_acron='', param_order=''):
        r = ''
        if data:
            issn, vol, issueno, suppl, fpage, order = data

            page_or_order = ''
            seq = ''
            if fpage.isdigit():
                if not int(fpage) == 0:
                    page_or_order = fpage
            elif '-' in fpage:
                p = fpage.split('-')
                if p[0].isdigit():
                    page_or_order = p[0]
                    seq = '-' + p[1]
            if page_or_order:
                page_or_order = fpage + seq
            else:
                page_or_order = '00000' + order
                page_or_order = page_or_order[-5:]

            if issueno:
                issueno = '00' + issueno
                issueno = issueno[-2:]

            if suppl:
                suppl = 's' + suppl if suppl != '0' else 'suppl'

            issueid = []
            for item in [vol, issueno, suppl]:
                if item != '' and item is not None:
                    issueid.append(item)
            issueid = '-'.join(issueid)

            r = '-'.join([issn, param_acron, issueid, page_or_order])

        return r

    def xml_data_image_names(self):
        #test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href']

        nodes = self.root.findall('.//*[graphic]')
        r = {}

        for n in nodes:
            if n.attrib.get('id') is not None:
                id = n.attrib.get('id', '')
                if '-' in id:
                    id = id[id.rfind('-')+1:]
                if n.tag == 'equation':
                    id = 'e' + id
                elif n.tag == 'inline-display':
                    id = 'i' + id
                else:
                    id = 'g' + id
                graphic_nodes = n.findall('graphic')

                for graphic_node in graphic_nodes:
                    for attrib_name in graphic_node.attrib:
                        if 'href' in attrib_name:
                            href = graphic_node.attrib.get(attrib_name)
                            r[href] = id
        return r

    def new_name_and_img_list(self, acron, alternative_id=''):
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        xml_images_list = self.xml_data_image_names()
        return (new_name, xml_images_list)


class XMLPkgMker:

    def __init__(self, src, scielo_pkg_files, pmc_pkg_files, acron, default_version, ctrl_filename=None, entities_table=None):
        if os.path.isfile(src) and src.endswith('.xml'):
            self.src_path = os.path.dirname(src)
            self.xml_filename = os.path.basename(src)
            self.xml_name = self.xml_filename.replace('.sgm.xml', '').replace('.xml', '')
            self.ctrl_filename = ctrl_filename
        else:
            self.src_path = src
            self.xml_filename = None
            self.xml_name = None
            self.ctrl_filename = None
        self.entities_table = entities_table
        self.scielo_pkg_files = scielo_pkg_files
        self.pmc_pkg_files = pmc_pkg_files

        self.acron = acron
        self.version_converter = _versions_.get(default_version, {}).get('sgm2xml')
        #_versions_[self.version]['sgm2xml']
        self.default_version = default_version
        self.src_copy_path = tempfile.mkdtemp()
        self.new_name_path = tempfile.mkdtemp()

        self.sci_validations = XMLValidations('scielo', default_version, self.entities_table)
        self.pmc_validations = XMLValidations('pmc', default_version)

    def _normalize_xml(self, input_filename, alternative_id):
        """
        Normalize XML content
        """
        f = open(input_filename, 'r')
        content = f.read()
        f.close()

        # convert_ent_to_cha
        content = convert_ent_to_char(content, self.entities_table)

        # fix problems of XML format
        if input_filename.endswith('.sgm.xml'):
            content = XMLFixer().fix(content)

        # get href of images and new name
        new_name = os.path.basename(input_filename).replace('.sgm.xml', '').replace('.xml', '')
        img_list = {}
        if xml_is_well_formed(content):
            new_name, img_list = XMLMetadata(content).new_name_and_img_list(self.acron, alternative_id)

            if input_filename.endswith('.sgm.xml'):
                content = xml_content_transform(content, self.version_converter)

        if xml_is_well_formed(content):
            f = open(self.new_name_path + '/' + new_name + '.xml', 'w')
            f.write(content)
            f.close()

        return [new_name, img_list]

    def _create_src_copy(self, selected_files):
        failures = []
        for filename in selected_files:
            shutil.copyfile(self.src_path + '/' + filename, self.src_copy_path + '/' + filename)
            if (filename.endswith('.tiff') or filename.endswith('.eps') or filename.endswith('.tif')):
                jpeg = filename[0:filename.rfind('.')] + '.jpg'
                if not os.path.exists(self.src_path + '/' + jpeg):
                    if IMG_CONVERTER:
                        if not img_to_jpeg(self.src_path + '/' + filename, self.src_copy_path):
                            failures.append(self.src_path + '/' + filename)
                    else:
                        failures.append(self.src_path + '/' + filename)

        if failures:
            f = open(self.scielo_pkg_files.report_path + '/not_converted_to_jpg.txt', 'w')
            f.write('\n'.join(failures))
            f.close()

    def _add_related_files_to_packages(self, related_files, curr_name, new_name):
        # copy <xml_file>.???
        for filename in [f for f in related_files if f.startswith(curr_name + '.')]:
            related_file = self.src_copy_path + '/' + filename
            new_filename = filename.replace(curr_name, new_name)
            shutil.copyfile(related_file, self.scielo_pkg_files.pkg_path + '/' + new_filename)
            shutil.copyfile(related_file, self.pmc_pkg_files.pkg_path + '/' + new_filename)

    def _add_img_to_packages(self, related_files, img_list, new_name):
        # copy image files which starts with <href>.
        #print(related_files)
        unmatched = []
        invalid_href = []
        for href, suffix in img_list.items():
            ext = href[href.rfind('.'):]
            if ext in ['.tif', '.eps', '.tiff', '.jpg']:
                invalid_href.append(href)
                href = href[0:href.find(ext)]

            matched_image_names = [f for f in related_files if f.startswith(href + '.')]
            for image_filename in matched_image_names:
                #print('  img file: ' + image_filename)
                ext = image_filename[image_filename.rfind('.'):]

                img_filename = self.src_copy_path + '/' + image_filename
                new_filename = new_name + '-' + suffix + ext
                #shutil.copyfile(img_filename, self.new_name_path + '/' + new_filename)
                shutil.copyfile(img_filename, self.scielo_pkg_files.pkg_path + '/' + new_filename)
                if not image_filename.endswith('.jpg'):
                    shutil.copyfile(img_filename, self.pmc_pkg_files.pkg_path + '/' + new_filename)
            if not matched_image_names:
                unmatched.append(href)
        if unmatched or invalid_href:
            message = ''
            if invalid_href:
                message += 'Do not use extension in href= inside the XML\n' + '\n'.join(invalid_href)
            if unmatched:
                message += 'Not found\n' + '\n'.join(unmatched)
            if self.scielo_pkg_files:
                f = open(self.scielo_pkg_files.report_path + '/images.err.txt', 'w')
                f.write(message)
                f.close()

    def manage_output_files(self, xml_filename, pkg_files, is_well_formed, is_dtd_valid, is_style_valid):
        if self.ctrl_filename:
            err_filename = self.ctrl_filename.replace('.ctrl', '.err')
            msg = ''
            if not is_well_formed:
                msg = 'Not well formed'
            elif not is_dtd_valid:
                msg = 'Not according to DTD'
            elif not is_style_valid:
                msg = 'Not valid style'
            if msg:
                f = open(err_filename, 'w')
                f.write(msg)
                f.close()
        else:
            if is_dtd_valid:
                os.unlink(pkg_files.dtd_validation_report)
            if is_style_valid:
                os.unlink(pkg_files.style_checker_report)
            if not is_well_formed:
                shutil.copyfile(xml_filename, pkg_files.dtd_validation_report)

    def _make_packages_for_one_file(self, xml_file, curr_name, related_files):
        print(curr_name)
        new_name, img_list = self._normalize_xml(self.src_copy_path + '/' + xml_file, curr_name)

        xml_filename = self.new_name_path + '/' + new_name + '.xml'

        self.scielo_pkg_files.name(curr_name, new_name)
        self.pmc_pkg_files.name(curr_name, new_name)

        xsl_new_name = new_name if new_name != curr_name else ''

        if os.path.exists(xml_filename):

            self._add_related_files_to_packages(related_files, curr_name, new_name)
            self._add_img_to_packages(related_files, img_list, new_name)
            img_path = self.scielo_pkg_files.pkg_path

            is_well_formed, is_dtd_valid, is_style_valid = self.sci_validations.check_list(xml_filename, self.scielo_pkg_files, img_path)
            self.manage_output_files(xml_filename, self.scielo_pkg_files, is_well_formed, is_dtd_valid, is_style_valid)

            if os.path.exists(self.scielo_pkg_files.xml_output):
                #dtd_validation_report = self.report_path + '/' + curr_name + '.err.txt'
                xml_filename = self.scielo_pkg_files.xml_output

                is_well_formed, is_dtd_valid, is_style_valid = self.pmc_validations.check_list(xml_filename, self.pmc_pkg_files, img_path, xsl_new_name)

                self.manage_output_files(xml_filename, self.pmc_pkg_files, is_well_formed, is_dtd_valid, is_style_valid)
                if self.ctrl_filename:
                    f = open(self.ctrl_filename, 'w')
                    f.write('Finished')
                    f.close()

                if os.path.exists(self.pmc_pkg_files.xml_output):
                    print('  Finished')
                else:
                    print('\nUnable to create ' + self.pmc_pkg_files.xml_output)
                    f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
                    f.write('\nUnable to create ' + self.pmc_pkg_files.xml_output)
                    f.close()
            else:
                print('Unable to create ' + self.scielo_pkg_files.xml_output)
                f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
                f.write('\nUnable to create ' + self.scielo_pkg_files.xml_output)
                f.close()
        else:
            print(curr_name + ' is not a well formed XML')
            f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
            f.write(curr_name + ' is not a well formed XML')
            f.close()

    def make_packages(self):
        if self.xml_filename:
            # only one file
            selected_files = [f for f in os.listdir(self.src_path) if f.startswith(self.xml_name)]
        else:
            selected_files = [f for f in os.listdir(self.src_path) if os.path.isfile(self.src_path + '/' + f)]
            #self._clean_folders()
        self._create_src_copy(selected_files)

        xml_files = [f for f in selected_files if f.endswith('.xml')]
        non_xml_files = [f for f in os.listdir(self.src_copy_path) if not f.endswith('.xml')]

        for xml_file in xml_files:
            curr_name = xml_file.replace('.sgm.xml', '').replace('.xml', '')
            related_files = [f for f in non_xml_files if f.startswith(curr_name)]
            #xml_file, selected_files_path, normalized_pck_path, curr_name, related_files

            self._make_packages_for_one_file(xml_file, curr_name, related_files)

        print('\n=======')
        print('\nGenerated packages in:\n' + '\n'.join([self.scielo_pkg_files.pkg_path, self.pmc_pkg_files.pkg_path, ]))
        for report_path in list(set([self.scielo_pkg_files.report_path, self.pmc_pkg_files.report_path, ])):
            if os.listdir(report_path):
                print('\nReports in: ' + report_path)
        print('\n==== END ===\n')

        shutil.rmtree(self.src_copy_path)
        shutil.rmtree(self.new_name_path)


def make_packages(src, acron, version='j1.0'):
    if not version in _versions_.keys():
        version = 'j1.0'
    doit = False
    ctrl_filename = None
    from datetime import datetime
    now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
    now = now[0:now.find('.')]
    if src.endswith('.sgm.xml'):
        version = 'j1.0'
        # src = serial/acron/issue/pmc/pmc_work/article/file.sgm.xml
        sgmxml_filename = src
        # sgmxml_path = serial/acron/issue/pmc/pmc_work/article
        sgmxml_path = os.path.dirname(src)
        # ctrl filename
        ctrl_filename = sgmxml_filename.replace('.sgm.xml', '.ctrl.txt')
        if os.path.exists(ctrl_filename):
            os.unlink(ctrl_filename)
        err_filename = sgmxml_filename.replace('.sgm.xml', '.err.txt')
        if os.path.exists(err_filename):
            os.unlink(err_filename)
        # pmc_path = serial/acron/issue/pmc
        pmc_path = os.path.dirname(os.path.dirname(sgmxml_path))
        # acron = acron
        acron = os.path.basename(os.path.dirname(os.path.dirname(pmc_path)))
        # other files path = serial/acron/issue/pmc/src or serial/acron/issue/pmc/pmc_src
        pmc_src = pmc_path + '/pmc_src'
        if os.path.isdir(pmc_path + '/pmc_src'):
            pmc_src = pmc_path + '/pmc_src'
        elif os.path.isdir(pmc_path + '/src'):
            pmc_src = pmc_path + '/src'
        else:
            os.makedirs(pmc_src)

        shutil.copyfile(sgmxml_filename, pmc_src + '/' + os.path.basename(sgmxml_filename))
        src = pmc_src + '/' + os.path.basename(sgmxml_filename)
        scielo_pkg_path = pmc_path + '/xml_package'
        pmc_pkg_path = pmc_path + '/pmc_package'
        report_path = sgmxml_path
        pmc_preview_path = sgmxml_path
        sci_preview_path = sgmxml_path
        doit = True
    elif src.endswith('.xml') and os.path.isfile(src):
        # xml packages maker
        path = os.path.dirname(src) + '_' + now
        scielo_pkg_path = path + '/scielo_package'
        pmc_pkg_path = path + '/pmc_package'
        report_path = path + '/errors'
        pmc_preview_path = None
        sci_preview_path = path + '/preview'
        doit = True
    elif os.path.isdir(src) and any([True for f in os.listdir(src) if f.endswith('.xml')]):
        # xml packages maker
        path = src + '_' + now
        scielo_pkg_path = path + '/scielo_package'
        pmc_pkg_path = path + '/pmc_package'
        report_path = path + '/errors'
        pmc_preview_path = None
        sci_preview_path = path + '/preview'
        doit = True
    if doit:
        finalized_fine = False
        scielo_pkg_files = ValidationFiles(scielo_pkg_path, report_path, sci_preview_path)
        pmc_pkg_files = ValidationFiles(pmc_pkg_path, report_path, pmc_preview_path, '.pmc')
        xml_pkg_mker = XMLPkgMker(src, scielo_pkg_files, pmc_pkg_files, acron, version, ctrl_filename, entities_table)
        try:
            xml_pkg_mker.make_packages()
            finalized_fine = True
        except:
            finalized_fine = False


def _call_make_packages(args, version):
    args = [arg.replace('\\', '/') for arg in args]
    script_name = args[0]

    if len(args) == 3:
        ign, src, acron = args
        if (os.path.isfile(src) and src.endswith('.xml')) or (os.path.isdir(src) and [f for f in os.listdir(src) if f.endswith('.xml')]):
            make_packages(src, acron, version)
        else:
            print('\n===== ATTENTION =====\n')
            print('ERROR: Incorrect parameters')
            print('\nUsage:')
            print('python ' + script_name + ' <src> <acron>')
            print('where:')
            print('  <src> = XML filename or path which contains XML files')
            print('  <acron> = journal acronym')

            print(src + ' is not a folder neither a XML file')
    elif len(args) == 2:
        ign, src = args
        if src.endswith('.sgm.xml'):
            make_packages(src, '', 'j1.0')
    else:
        print('ERROR: Incorrect parameters')
        print('\nUsage:')
        print('python ' + script_name + ' <src> <acron>')
        print('where:')
        print('  <src> = XML filename or path which contains XML files')
        print('  <acron> = journal acronym')


def call_make_packages(args, version):
    if DEBUG == 'ON':
        _call_make_packages(args, version)
    else:
        try:
            _call_make_packages(args, version)
        except Exception as inst:
            print('\n===== ATTENTION =====\nThere was an unexpected error.\n Please, report it to roberta.takenaka@scielo.org or at https://github.com/scieloorg/PC-Programs/issues')
            print(inst)


###
_versions_ = configure_versions_location()
entities_table = EntitiesTable(ENTITIES_TABLE_FILENAME)
