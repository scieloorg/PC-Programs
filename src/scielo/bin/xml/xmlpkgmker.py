# coding=utf-8

import random
import os
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
                    #self.table_number2char['&#x' + hex_ent[hex_ent.find('x')+1:].upper() + ';'] = char

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


def convert_entname(content, entities_table=None):
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

        content = content.replace('&#', PREFIX_ENT + '#')

        if '&' in content:
            if entities_table:
                while '&' in content:
                    ent = content[content.find('&'):]
                    ent = ent[0:ent.find(';')+1]

                    char = entities_table.ent2chr(ent)
                    if char == ent:
                        content = content.replace(ent, ent.replace('&', PREFIX_ENT))
                        not_found_named.append(ent)
                    else:
                        content = content.replace(ent, char)

        if not_found_named:
            f = open('unknown_ent_named.txt', 'a+')
            f.write('\n'.join(not_found_named))
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
    if os.path.exists(temp_result_filename):
        print(result_filename + ' was created fine.')
    else:
        f = open(temp_result_filename, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(xml_filename)
        f.write(xsl_filename)
        f.write(result_filename)
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
class XMLStr:

    def __init__(self, content):
        self.content = content

    def fix_dtd_location(self, dtd_filename, doctype):
        if not dtd_filename in self.content:
            if not '<?xml ' in self.content:
                self.content = '<?xml version="1.0" encoding="utf-8"?>\n' + self.content

            if '<!DOCTYPE' in self.content:
                old_doctype = self.content[self.content.find('<!DOCTYPE'):]
                old_doctype = old_doctype[0:old_doctype.find('>')+1]
                self.content = self.content.replace(old_doctype, '')
            if not '<!DOCTYPE' in self.content:
                self.content = self.content.replace('\n<article ', doctype.replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')

    def fix(self):
        self.content = self.content[0:self.content.rfind('>')+1]
        self.content = self.content[self.content.find('<'):]
        if not xml_is_well_formed(self.content):
            f = open('fix1.xml', 'w')
            f.write(self.content)
            f.close()
            self._fix_style_tags()
            if not xml_is_well_formed(self.content):
                f = open('fix2.xml', 'w')
                f.write(self.content)
                f.close()
                self._fix_open_close()
                if not xml_is_well_formed(self.content):
                    f = open('fix3.xml', 'w')
                    f.write(self.content)
                    f.close()

    def _fix_open_close(self):
        changes = []
        parts = self.content.split('>')
        for s in parts:
            if '<' in s:
                if not '</' in s and not '<!--' in s and not '<?' in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and not '=' in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            print(change)
            self.content = self.content.replace('<' + test + '>', '[' + test + ']')

    def _fix_style_tags(self):
        rcontent = self.content
        tags = ['italic', 'bold', 'sub', 'sup']
        tag_list = []
        for tag in tags:
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')
        if content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            self.content = self._fix_problem(tag_list, parts)

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


class ValidationFolders:

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

    def joined(self):
        from StringIO import StringIO

        output = etree.ElementTree().parse(StringIO('<articles></articles>'))

        for item in [f for f in os.listdir(self.pkg_path) if f.endswith('.xml')]:
            xml = self.pkg_path + '/' + item
            print(xml)
            try:
                article = etree.parse(open(xml))
                art = article.getroot().findall('.')

                if art:
                    art = art[0]
                    art.attrib['filename'] = item
                    output.append(art)
            except Exception as inst:
                output.append(etree.ElementTree().parse(StringIO('<error>%s</error>' % xml)))
                print(inst)
            #e_tree = etree.ElementTree(output)
            #e_tree.write('f.xml')
            #etree.tostring(ouput)
        return output

    def generate_reports(self):
        lists = []
        lists.append(('authors.html', ['.//name'], ['suffix', 'prefix', 'given-names', 'surname']))
        lists.append(('publishers.html', ['.//element-citation'], ['publisher-name', 'publisher-loc']))
        lists.append(('locations.html', ['.//publisher-loc'], None))
        lists.append(('affs.html', ['.//aff'], ['institution[@content-type=orgname"]', 'institution[@content-type="orgdiv1"]', 'institution[@content-type="orgdiv2"]', 'institution[@content-type="orgdiv3"]', 'named-content[@content-type="city"]', 'country']))
        
        report = DataReport()
        for report_filename, xpath_list, children_xpath in lists:
            data = report._format_list(self.joined(), xpath_list, children_xpath)
            report.print_report(data, children_xpath, self.report_path + '/' + report_filename)


class ValidationFiles:
    def __init__(self, folders, curr_name, new_name, xml_output_path=None, suffix=''):
        self.folders = folders

        #self.ctrl_filename = ctrl_filename

        self.dtd_validation_report = self.folders.report_path + '/' + curr_name + suffix + '.dtd.txt'
        self.style_checker_report = self.folders.report_path + '/' + curr_name + suffix + '.rep.html'

        if self.folders.preview_path == self.folders.pkg_path:
            self.html_preview = self.folders.preview_path + '/' + new_name + '.html'
        elif self.folders.preview_path:
            self.html_preview = self.folders.preview_path + '/' + curr_name + suffix + '.xml.html'
        else:
            self.html_preview = None
        if xml_output_path:
            self.xml_output = xml_output_path + '/' + new_name + '.xml'
        else:
            self.xml_output = self.folders.pkg_path + '/' + new_name + '.xml'

    def manage_result(self, ctrl_filename, is_well_formed, is_dtd_valid, is_style_valid):
        if ctrl_filename:
            err_filename = ctrl_filename.replace('.ctrl', '.err')
            if not is_well_formed:
                #shutil.copyfile(xml_filename, err_filename)
                f = open(err_filename, 'a+')
                f.write('manage_result1.XML is not well formed')
                f.close()
            elif not is_dtd_valid and os.path.exists(self.dtd_validation_report):
                shutil.copyfile(self.dtd_validation_report, err_filename)
            f = open(ctrl_filename, 'w')
            f.write('Finished')
            f.close()
        else:
            if is_dtd_valid:
                os.unlink(self.dtd_validation_report)
            if is_style_valid:
                os.unlink(self.style_checker_report)
            if not is_well_formed:
                f = open(self.dtd_validation_report, 'a+')
                f.write('manage_result2.XML is not well formed')
                f.close()


class XMLValidator:
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

                report_ok = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))

                if report_ok:
                    self.report('Validation report. No errors/warnings: found. Read ' + style_checker_report)
                else:
                    self.report('Validation report. Some errors/warnings were found. Read ' + style_checker_report)
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
                r = [False, False, False]
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
            content = convert_entname(content, self.entities_table)
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
                xml_str = XMLStr(content)
                xml_str.fix_dtd_location(self.dtd_filename, self.doctype)
                content = xml_str.content

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

        #self.manage_result(xml_filename, pkg_files, is_well_formed, is_dtd_valid, is_style_valid)
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
            print(data)
            page_or_order = ''
            seq = ''
            if not fpage.isdigit():
                if not int(fpage) == 0:
                    page_or_order = fpage
            elif '-' in fpage:
                p = fpage.split('-')
                if p[0].isdigit():
                    page_or_order = p[0]
                    seq = '-' + p[1]
            print(page_or_order)
            if page_or_order:
                page_or_order = fpage + seq
            else:
                if not order.replace('0', ''):
                    order = param_order
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

    def xml_data_href_filenames(self):
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

    def xml_data_href_names(self):
        #test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href']

        nodes = self.root.findall('.//supplementary[@xlink:href]')
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

    def new_names_and_embedded_files(self, acron, alternative_id=''):
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        href_filenames = self.xml_data_href_filenames()
        return (new_name, href_filenames)


class DataReport(object):

    def print_report(self, data, columns, report_filename):
        print(columns)
        if not columns:
            columns = ['value']

        html = '<html><header><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></header><body><table><tr><td>filename</td><td></td>%s</tr>' % ''.join(['<td>%s</td>' % label for label in columns])
        for row in data:
            r = '<td>%s</td><td>%s</td>' % (row['id'], row['label'])
            r += ''.join(['<td>%s</td>' % row.get(column_name, '') for column_name in columns])
            html += '<tr>%s</tr>' % r
            html += '<!-- ' + ' - '.join([ k + '=' + v for k, v in row.items()]) + ' -->'
        html += '</table></body></html>'

        import codecs

        f = codecs.open(report_filename, 'w', 'utf-8')
        f.write(html)
        f.close()

    def _format_list(self, xml, xpath_list, children_xpath):
        rows = []
        for doc in xml.findall('article'):
            filename = doc.attrib.get('filename', '?')
            parts = ['.//journal-meta', './/article-meta', './/ref']
            for part in parts:

                part_nodes = doc.findall(part)

                for part_node in part_nodes:
                    label = part[3:]
                    if part == './/ref':
                        label = part_node.attrib.get('id', '?')
                  
                    for xpath in xpath_list:
                        results = self._get_from_xml(part_node, xpath, children_xpath)
                        for item in results:
                            item.update({'id': filename, 'label': label})
                            rows.append(item)
        return rows

    def _get_from_xml(self, start_node, xpath, children_xpath):
        results = []
        nodes = start_node.findall(xpath)
        for node in nodes:
            data = {}
            print(children_xpath)
            if children_xpath:
                for child_xpath in children_xpath:
                    child_nodes = node.findall(child_xpath)
                    key = child_xpath[child_xpath.rfind('/'):] if '/' in child_xpath else child_xpath
                    
                    data[key] = child_nodes[0].text if child_nodes else ''
            else:

                key = xpath[xpath.rfind('/'):] if '/' in xpath else xpath
                data[key] = node[0].text if node else ''
            results.append(data)
        return results


class Article:
    def __init__(self, xml_path, xml_filename, wrk_path, new_path, report_path):
        self.is_sgmxml = xml_filename.endswith('.sgm.xml')
        self.xml_path = xml_path
        self.xml_filename = xml_filename

        self.xml_name = xml_filename.replace('.sgm.xml', '').replace('.xml', '')
        self.wrk_path = wrk_path + '/' + self.xml_name

        self.new_name = None
        self.new_path = new_path

        self.report_path = report_path
        self.normalized_xml_filename = ''

    def create_work_folder(self, jpg_err_filename):
        if not os.path.exists(self.wrk_path):
            os.makedirs(self.wrk_path)

        not_jpeg = []
        for filename in os.listdir(self.xml_path):
            if filename.startswith(self.xml_name + '.') or filename.startswith(self.xml_name + '-'):
                shutil.copyfile(self.xml_path + '/' + filename, self.wrk_path + '/' + filename)
                if filename.endswith('.tiff') or filename.endswith('.eps') or filename.endswith('.tif'):
                    jpeg = filename[0:filename.rfind('.')] + '.jpg'
                    if not os.path.exists(self.xml_path + '/' + jpeg):
                        if IMG_CONVERTER:
                            if not img_to_jpeg(self.xml_path + '/' + filename, self.wrk_path):
                                not_jpeg.append(self.xml_path + '/' + filename)
                        else:
                            not_jpeg.append(self.xml_path + '/' + filename)
        if not_jpeg:
            f = open(self.report_path + '/' + jpg_err_filename, 'w')
            f.write('\n'.join(not_jpeg))
            f.close()

    def make_article_packages(self, scielo_folder, pmc_folder):

        if self.normalized_xml_filename:

            self.scielo_files = ValidationFiles(scielo_folder, self.xml_name, self.new_name, pmc_folder.pkg_path)
            self.pmc_files = ValidationFiles(pmc_folder, self.xml_name, self.new_name, None, '.pmc')

            self._add_related_files_to_packages([scielo_folder.pkg_path, pmc_folder.pkg_path])
            self._add_href_files_to_packages(scielo_folder.pkg_path, pmc_folder.pkg_path, scielo_folder.report_path)

            #shutil.copyfile(self.normalized_xml_filename, scielo_folder.pkg_path + '/' + self.new_name + '.xml')
        else:
            print('Unable to make article package because of missing normalized_xml_filename')

    def _add_related_files_to_packages(self, package_paths):
        # copy <xml_file>.???
        for filename in os.listdir(self.wrk_path):
            new_filename = filename.replace(self.xml_name, self.new_name)
            for pkg_path in package_paths:
                shutil.copyfile(self.wrk_path + '/' + filename, pkg_path + '/' + new_filename)

    def _normalize_href_list(self):
        invalid_href = []
        fixed = {}
        for href, suffix in self.href_files_list.items():
            ext = href[href.rfind('.'):]
            if ext in ['.tif', '.eps', '.tiff', '.jpg', '.pdf', '.html', '.htm'] or len(ext) == 4:
                invalid_href.append(href)
                href = href[0:href.find(ext)]
                fixed[href] = suffix
        self.href_files_list = fixed
        return invalid_href

    def _add_href_files_to_packages(self, scielo_pkg_path, pmc_pkg_path, report_path):
        missing_files = []
        invalid_href = self._normalize_href_list()

        related_files = os.listdir(self.wrk_path)

        for href, suffix in self.href_files_list.items():
            matched_files = [f for f in related_files if f.startswith(href + '.')]
            for filename in matched_files:
                #print('  img file: ' + filename)
                ext = filename[filename.rfind('.'):]

                matched = self.wrk_path + '/' + filename
                new_filename = self.xml_name + '-' + suffix + ext

                shutil.copyfile(matched, scielo_pkg_path + '/' + new_filename)
                if not filename.endswith('.jpg'):
                    shutil.copyfile(matched, pmc_pkg_path + '/' + new_filename)
            if not matched_files:
                missing_files.append(href)
        if missing_files or invalid_href:
            message = ''
            if invalid_href:
                message += 'Do not use extension in href= inside the XML\n' + '\n'.join(invalid_href)
            if missing_files:
                message += 'Not found\n' + '\n'.join(missing_files)
            if report_path:
                f = open(report_path + '/href.err.txt', 'w')
                f.write(message)
                f.close()


class XMLPackagesMaker:

    def __init__(self, sci_validator, pmc_validator, acron, default_version, entities_table):
        self.version_converter = _versions_.get(default_version, {}).get('sgm2xml')
        self.entities_table = entities_table
        self.acron = acron

        self.sci_validator = sci_validator
        self.pmc_validator = pmc_validator

    def _normalize_xml(self, article):
        """
        Normalize XML content
        """
        f = open(article.wrk_path + '/' + article.xml_filename)
        content = f.read()
        f.close()

        # convert_ent_to_cha
        content = convert_entname(content, self.entities_table)

        # fix problems of XML format
        if article.is_sgmxml:
            xml_fix = XMLStr(content)
            xml_fix.fix()
            content = xml_fix.content

        # get href of images and new name
        article.new_name = article.xml_name
        article.href_files_list = {}
        if xml_is_well_formed(content):
            article.new_name, article.href_files_list = XMLMetadata(content).new_names_and_embedded_files(self.acron, article.xml_name)

            if article.is_sgmxml:
                content = xml_content_transform(content, self.version_converter)

        if xml_is_well_formed(content):
            article.normalized_xml_filename = article.new_path + '/' + article.new_name + '.xml'

            f = open(article.normalized_xml_filename, 'w')
            f.write(content)
            f.close()

    def make_packages(self, xml_filename, ctrl_filename, xml_path, wrk_path, scielo_folder, pmc_folder):

        files = [xml_filename] if xml_filename else [f for f in os.listdir(xml_path) if f.endswith('.xml')]

        report_path = scielo_folder.report_path
        new_path = scielo_folder.pkg_path

        for xml_filename in files:
            print(xml_filename)

            article = Article(xml_path, xml_filename, wrk_path, new_path, report_path)
            article.create_work_folder('jpg_missing.txt')

            self._normalize_xml(article)

            article.make_article_packages(scielo_folder, pmc_folder)
            # else:
            # print(xml_name + ' is not a well formed XML')
            # f = open(scielo_files.dtd_validation_report, 'a+')
            # f.write(xml_name + ' is not a well formed XML')
            # f.close()
            self.validate_packages(article, ctrl_filename)

        scielo_folder.generate_reports()

        print('\n=======')
        print('\nGenerated packages in:\n' + '\n'.join([scielo_folder.pkg_path, pmc_folder.pkg_path, ]))
        for report_path in list(set([scielo_folder.report_path, pmc_folder.report_path, ])):
            if os.listdir(report_path):
                print('\nReports in: ' + report_path)
        print('\n==== END ===\n')

    def validate_packages(self, article, ctrl_filename):
        xsl_new_name = article.new_name if article.new_name != article.xml_name else ''
        img_path = article.scielo_files.folders.pkg_path

        is_well_formed, is_dtd_valid, is_style_valid = self.sci_validator.check_list(article.normalized_xml_filename, article.scielo_files, img_path)
        article.scielo_files.manage_result(ctrl_filename, is_well_formed, is_dtd_valid, is_style_valid)

        if os.path.exists(article.scielo_files.xml_output):
            #dtd_validation_report = article.report_path + '/' + xml_name + '.err.txt'
            article.normalized_xml_filename = article.scielo_files.xml_output

            is_well_formed, is_dtd_valid, is_style_valid = self.pmc_validator.check_list(article.normalized_xml_filename, article.pmc_files, img_path, xsl_new_name)

            article.pmc_files.manage_result(ctrl_filename, is_well_formed, is_dtd_valid, is_style_valid)

            if os.path.exists(article.pmc_files.xml_output):
                print('  Finished')
            else:
                print('\nUnable to create ' + article.pmc_files.xml_output)
                f = open(article.scielo_files.dtd_validation_report, 'a+')
                f.write('\nUnable to create ' + article.pmc_files.xml_output)
                f.close()
        else:
            print('Unable to create ' + article.scielo_files.xml_output)
            f = open(article.scielo_files.dtd_validation_report, 'a+')
            f.write('\nUnable to create ' + article.scielo_files.xml_output)
            f.close()
        

def setup_for_markup(sgmxml_filename):
    # sgmxml_path = serial/acron/issue/pmc/pmc_work/article
    sgmxml_path = os.path.dirname(sgmxml_filename)

    # pmc_path = serial/acron/issue/pmc
    pmc_path = os.path.dirname(os.path.dirname(sgmxml_path))

    # acron = acron
    acron = os.path.basename(os.path.dirname(os.path.dirname(pmc_path)))

    # other files path = serial/acron/issue/pmc/src or serial/acron/issue/pmc/pmc_src
    pmc_src = pmc_path + '/src'
    if not os.path.isdir(pmc_src):
        pmc_src = pmc_path + '/pmc_src'
    if not os.path.isdir(pmc_src):
        os.makedirs(pmc_src)

    shutil.copyfile(sgmxml_filename, pmc_src + '/' + os.path.basename(sgmxml_filename))

    src = pmc_src + '/' + os.path.basename(sgmxml_filename)
    scielo_pkg_path = pmc_path + '/xml_package'
    pmc_pkg_path = pmc_path + '/pmc_package'
    report_path = sgmxml_path
    preview_path = None #sgmxml_path
    wrk_path = sgmxml_path

    return (src, acron, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def setup_for_package_maker(src, now):
    if os.path.isdir(src):
        path = src + '_' + now
    else:
        path = os.path.dirname(src) + '_' + now

    scielo_pkg_path = path + '/scielo_package'
    pmc_pkg_path = path + '/pmc_package'
    report_path = path + '/errors'
    wrk_path = path + '/wrk'
    preview_path = None
    return (scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def check_inputs(args):
    args = [arg.replace('\\', '/') for arg in args]
    script_name = args[0] if len(args) > 0 else ''
    r = False

    src = ''
    acron = ''
    task = ''

    if len(args) == 2:
        ign, src = args
        acron = ''
        r = os.path.isfile(src) and src.endswith('.sgm.xml')
        task = 'markup'
    elif len(args) == 3:
        ign, src, acron = args
        if (os.path.isfile(src) and src.endswith('.xml')):
            task = 'file'
            r = True
        elif (os.path.isdir(src) and [f for f in os.listdir(src) if f.endswith('.xml')]):
            task = 'folder'
            r = True
    if not r:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python ' + script_name + ' <src> <acron>')
        messages.append('where:')
        messages.append('  <src> = XML filename or path which contains XML files')
        messages.append('  <acron> = journal acronym')
        task = '\n'.join(messages)
    return (src, acron, task)


def call_make_packages(args, version):
    src, acron, task = check_inputs(args)
    if task in ['markup', 'folder', 'file']:
        if task == 'markup':
            version = 'j1.0'
            # ctrl filename
            ctrl_filename = src.replace('.sgm.xml', '.ctrl.txt')
            #err_filename = src.replace('.sgm.xml', '.err.txt')
            src, acron, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = setup_for_markup(src)
            xml_path = os.path.dirname(src)
            xml_filename = os.path.basename(src)
        else:
            if task == 'folder':
                xml_path = src
                xml_filename = None
            else:
                xml_path = os.path.dirname(src)
                xml_filename = os.path.basename(src)

            from datetime import datetime
            now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
            now = now[0:now.find('.')]

            ctrl_filename = None
            scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = setup_for_package_maker(src, now)

        scielo_folder = ValidationFolders(scielo_pkg_path, report_path, preview_path)
        pmc_folder = ValidationFolders(pmc_pkg_path, report_path, preview_path, '.pmc')

        sci_validator = XMLValidator('scielo', version, entities_table)
        pmc_validator = XMLValidator('pmc', version)

        xml_pkg_mker = XMLPackagesMaker(sci_validator, pmc_validator, acron, version, entities_table)
        xml_pkg_mker.make_packages(xml_filename, ctrl_filename, xml_path, wrk_path, scielo_folder, pmc_folder)
    else:
        print(task)


###
_versions_ = configure_versions_location()
entities_table = EntitiesTable(ENTITIES_TABLE_FILENAME)
