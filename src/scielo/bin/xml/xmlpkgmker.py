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


def log_errors(err_filename, label, files):
    files = [item for item in files if item is not None]
    if len(files) > 0:
        f = open(err_filename, 'a+')
        f.write('\n\n%s:\n%s\n%s' % (label, '=' * len(label), '\n'.join(files)))
        f.close()


def log_message(filename, message):
    if message:
        f = open(filename, 'a+')
        f.write(message + '\n')
        f.close()


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


def convert_entities(content, entities_table=None):
    return convert_ent_to_char(content, entities_table)
    #return convert_entname(content, entities_table)


def convert_entname(content, entities_table=None):
    def prefix_ent(N=7):
        return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

    not_found_named = []

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
            print('XML is not well formed')
            print(e)
            r = None
    else:
        try:
            r = etree.parse(content)
        except Exception as e:
            print('XML is not well formed')
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
    name = os.path.basename(result_filename)

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)
    cmd = JAVA_PATH + ' -jar ' + JAR_TRANSFORM + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)

    print('Creating ' + name)
    os.system(cmd)
    #print(cmd)
    if not os.path.exists(temp_result_filename):
        print('  ERROR: Unable to create it.')

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
        if self.content != rcontent:
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
            #print(data)
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
            #print(page_or_order)
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


class PkgReport(object):

    def __init__(self, pkg_path, report_path):
        self.pkg_path = pkg_path
        self.report_path = report_path
        self.content_validations = []
        for filename in [f for f in os.listdir(self.pkg_path) if f.endswith('.xml')]:
            self.content_validations.append(ContentValidation(etree.parse(open(self.pkg_path + '/' + filename)), filename))
        self.lists = []

        self.lists.append(('authors.html', ['suffix', 'prefix', 'given-names', 'surname'], ['given-names', 'surname']))
        self.lists.append(('publisher.html', ['type', 'publisher-name', 'publisher-loc'], []))
        self.lists.append(('source.html', ['type', 'source', 'year'], ['type', 'source', 'year']))
        self.lists.append(('affs.html', ['orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3', 'city', 'state', 'country'], ['orgname']))

    def generate_articles_report(self, include_lists_content=False):
        expected_journal_meta = {}
        order_list = {}
        doi_list = {}
        doi_is_duplicated = []
        order_is_zero = []
        order_is_duplicated = []
        order_ok = {}
        unordered = {}
        jm = ''
        html_report = HTMLReport()

        for content_validation in self.content_validations:
            if expected_journal_meta == {}:
                for k, v in content_validation.issue_meta.items():
                    expected_journal_meta[k] = v
            expected_files = [f[0:f.rfind('.')] for f in os.listdir(self.pkg_path)]

            order = content_validation.article_meta.get('order', 0)
            if order == 0:
                order_is_zero.append(content_validation.article_meta['filename'])
                row_idx = content_validation.article_meta['filename']
            else:
                if order in order_list.keys():
                    order_list[order].append(content_validation.article_meta['filename'])
                    row_idx = content_validation.article_meta['filename']
                    order_is_duplicated.append(order)
                else:
                    order_list[order] = []
                    order_list[order].append(content_validation.article_meta['filename'])
                    row_idx = '00000' + str(order)
                    row_idx = row_idx[-5:]

            doi = content_validation.article_meta.get('doi', None)
            if doi:
                if doi in doi_list.keys():
                    doi_list[doi].append(content_validation.article_meta['filename'])
                    doi_is_duplicated.append(doi)
                else:
                    doi_list[doi] = []
                    doi_list[doi].append(content_validation.article_meta['filename'])

            content_validation.validations(expected_journal_meta, expected_files)

            result = self._report_article_meta(content_validation) + self._report_article_messages(content_validation)

            if include_lists_content:
                for report_filename, columns, required in self.lists:
                    items = self.data_for_list(report_filename, content_validation)
                    rows = self.data_in_table_format(content_validation.article_meta['filename'], items, columns, required)
                    result += '<div class="list"><h1>' + report_filename.replace('.html', '') + '</h1>' + html_report.in_table_format(rows, columns) + '</div>'

            if row_idx.isdigit():
                order_ok[row_idx] = '<div class="article">' + result + '</div>'
            else:
                unordered[row_idx] = '<div class="article">' + result + '</div>'
            if not jm:
                jm = self._report_journal_meta(content_validation)

        # doi, order, journal, sorted, unsorted.
        r = jm + '<div class="duplicated_messages">'
        for duplicated in doi_is_duplicated:
            r += '<p class="error">DOI duplicated: %s at %s</p>' % (duplicated, ', '.join(doi_list[duplicated]))
        for duplicated in order_is_duplicated:
            r += '<p class="error">order duplicated: %s at %s</p>' % (duplicated, ', '.join(order_list[duplicated]))
        r += '</div>'

        keys = order_ok.keys()
        keys.sort()
        for key in keys:
            r += order_ok[key]

        keys = unordered.keys()
        keys.sort()
        for key in keys:
            r += unordered[key]

        if r:
            
            errors = len(r.split('ERROR:')) - 1
            warnings = len(r.split('WARNING:')) - 1
            statistics = '<div class="statistics"><p>Total of errors = %s</p><p>Total of warnings = %s</p></div>' % (str(errors), str(warnings))
            html_report._html(self.report_path + '/toc2.html', '', html_report._css('toc') + html_report._css('datareport'), statistics + r)

    def data_for_list(self, report_filename, content_validation):
        items = []
        if report_filename == 'authors.html':
            items = content_validation.article_meta['author']
            for ref in content_validation.refs:
                items += ref['author']
        elif report_filename == 'publisher.html':
            items = [content_validation.issue_meta] + content_validation.refs
        elif report_filename == 'source.html':
            items = content_validation.refs
        elif report_filename == 'affs.html':
            items = content_validation.article_meta['aff']
        return items

    def generate_lists(self):
        report = HTMLReport()

        for report_filename, columns, required in self.lists:
            print(report_filename)
            rows = []
            for content_validation in self.content_validations:
                items = self.data_for_list(report_filename, content_validation)
                rows += self.data_in_table_format(content_validation.article_meta['filename'], items, columns, required)

            report._html(self.report_path + '/' + report_filename, report_filename, report._css('datareport'), report.in_table_format(rows, columns))

    def data_in_table_format(self, filename, items, columns, required_items):
        rows = []
        print(items)
        for item in items:
            
            row = {'id': filename, 'label': item.get('id', '')}
            for child in columns:
                row[child] = item.get(child, '')
                if row[child] == '':
                    if child in required_items:
                        row[child] = 'ERROR: Required data'
            rows.append(row)
        return rows

    def _report_journal_meta(self, content_validation):
        data = '<div class="issue">'
        data += '<h1>%s, %s (%s)</h1>' % (content_validation.issue_meta.get('journal-title', ''), content_validation.issue_meta.get('volume', ''), content_validation.issue_meta.get('issue', ''))
        data += '<h2>%s</h2>' % content_validation.issue_meta.get('nlm-ta', '')
        for item in ['eissn', 'pissn', 'publisher-name']:
            s = content_validation.issue_meta.get(item, '')
            if not s:
                s = ''
            data += '<p>' + item + ': ' + s + '</p>'
        data += '</div>'
        return data

    #xxxx
    def _report_article_meta(self, content_validation):
        data = '<div class="article-data">'
        data += '<p class="filename">%s</p>' % content_validation.article_meta.get('filename', '')
        data += '<h1>%s</h1>' % content_validation.article_meta.get('subject', '')
        data += '<p class="article-type">%s</p>' % content_validation.article_meta.get('article-type', '')
        data += '<h2>[%s] %s</h2>' % (content_validation.article_meta.get('lang', '(missing language)'), content_validation.article_meta.get('article-title', ''))
        for lang, title in content_validation.article_meta.get('trans-title', {}).items():
            data += '<h3> [%s] %s</h3>' % (lang, title)

        data += '<p class="doi">%s</p>' % content_validation.article_meta.get('doi', '')

        for item in ['date-epub', 'date-ppub', 'date-epub-ppub']:
            data += '<p>' + item + ': ' + str(content_validation.article_meta.get(item, '')) + '</p>'
        data += '<p class="id">%s [fpage: <span class="fpage">%s</span> | fpage/@seq: <span class="fpage_seq">%s</span> | .//article-id[@pub-id-type="other"]: <span class="other-id">%s</span>]</p>' % (content_validation.article_meta['order'], content_validation.article_meta.get('fpage', ''), content_validation.article_meta.get('fpage_seq', ''), content_validation.article_meta.get('other id', ''))
        data += '<p class="fpage">pages: %s</p>' % (content_validation.article_meta.get('fpage', '') + '-' + content_validation.article_meta.get('lpage', ''))

        #data += '<p class="authors"></p>' % content_validation._format_as_table(content_validation.article_meta['author'], ['given-names', 'surname', 'prefix', 'suffix'])
        items = []
        for author in content_validation.article_meta.get('author', []):
            prefix = '(%s) ' % author['prefix'] if author.get('prefix', None) is not None else ''
            suffix = ' (%s)' % author['suffix'] if author.get('suffix', None) is not None else ''

            if not author['surname']:
                author['surname'] = 'ERROR: missing surname'
            if not author['given-names']:
                author['given-names'] = 'ERROR: missing name'

            items.append(author['surname'] + suffix + ', ' + prefix + author['given-names'])
        data += '<p class="authors">%s</p>' % '; '.join(items)

        data += '<p class="authors">%s</p>' % '; '.join(content_validation.article_meta.get('collab', []))

        data += '<p class="affs">%s</p>' % self._format_as_table(content_validation.article_meta['aff'], ['xml', 'orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3', 'city', 'state', 'country', 'email'])

        if content_validation.article_meta.get('abstract', ''):
            data += '<p class="abstract"> [%s] %s</p>' % (content_validation.article_meta.get('lang', '??'), content_validation.article_meta.get('abstract', ''))

        for lang, abstract in content_validation.article_meta.get('trans-abstract', {}).items():
            data += '<p class="trans-abstract"> [%s] %s</p>' % (lang, abstract)

        kwg = content_validation.article_meta.get('kwd-group', {})
        if not kwg == {}:
            for lang, kwd_group in kwg.items():
                kwd = '; '.join(kwd_group) if kwd_group else ''
                data += '<p class="kwd-group"> [%s] %s</p>' % (lang, kwd)

        data += '<p class="ack">%s</p><p class="funding">%s</p>' % (content_validation.article_meta['ack'], content_validation.article_meta['award-id'])

        data += '</div>'

        return data

    def _format_messages(self, messages):
        if messages is None:
            return ''
        elif isinstance(messages, str):
            return self._eval(messages)
        elif isinstance(messages, list):
            return ''.join([self._format_messages(item) for item in messages])
        elif isinstance(messages, dict):
            ref_messages = ''
            for label, msg in messages.items():
                if not label in ['id', 'xml']:
                    if isinstance(msg, str):
                        ref_messages += self._eval(msg)
                    elif msg is not None:
                        ref_messages += ''.join([self._format_messages(m) for m in msg])
            r = ''
            if not ref_messages == '':
                r = '<div class="group">'
                if 'id' in messages.keys():
                    r += '<p class="group-id">%s</p>' % messages['id']
                r += ref_messages
                if 'xml' in messages.keys():
                    r += '<p class="xml">%s</p>' % messages['xml'].replace('<', '&lt;').replace('>', '&gt;')
                r += '</div>'
            return r

    def _report_article_messages(self, content_validation, issue_msg=False):
        # self.article_meta_validations = {}
        # self.files_validations = ''
        # self.issue_meta_validations = None
        # self.refs_validations = []
        messages = []
        if issue_msg:
            messages.append(self._format_messages(content_validation.issue_meta_validations))
        messages.append(self._format_messages(content_validation.article_meta_validations))
        messages.append(self._format_messages(content_validation.files_validations))
        messages.append(self._format_messages(content_validation.refs_validations))
        return '<div class="article-messages">%s</div>' % ''.join(messages)

    def _report_issue_messages(self, content_validation):
        # self.article_meta_validations = {}
        # self.files_validations = ''
        # self.issue_meta_validations = None
        # self.refs_validations = []
        messages = []
        messages.append(self._format_messages(content_validation.issue_meta_validations))
        #messages.append(more)
        return '<div class="issue-messages">%s</div>' % ''.join(messages)

    def _format_result(self, result):
        return [self._eval(v) for k, v in result.items() if not v == self._eval(v)]

    def _format_as_table(self, data, columns):
        r = '<div class="CSSTableGenerator"><table>'
        r += '<tr>'
        for col in columns:    
            r += '<td>%s</td>' % col
        r += '</tr>'
        for item in data:
            r += '<tr>'
            for col in columns:
                if col == 'xml':
                    r += '<td>%s</td>' % item.get(col, '').replace('<', '&lt;').replace('>', '&gt;')
                else:
                    r += '<td>%s</td>' % item.get(col, '')
            r += '</tr>'
        r += '</table></div>'
        return r

    def _eval(self, data):
        cls = 'warning' if 'WARNING' in data else 'error' if 'ERROR' in data else None
        if cls is None:
            return str(data)
        else:
            icon = ' ! ' if cls == 'warning' else ' X '
            return '<p class="p-%s"><span class="icon-%s"> %s </span><span class="text-%s"> %s</span></p>' % (cls, cls, icon, cls, data)


class HTMLReport(object):
    def __init__(self):
        f = open(CONFIG_VERSIONS_PATH + '/v3.0/xsl/scielo-style/datareport.css')
        self.css_content = f.read()
        f.close()

    def _css(self, name):
        f = open(CONFIG_VERSIONS_PATH + '/v3.0/xsl/scielo-style/' + name + '.css')
        css = f.read()
        f.close()
        return css

    def _table_(self, table_header, table_rows):
        return '<div class="CSSTableGenerator"><table>%s%s</table></div>' % (table_header, table_rows)

    def _table_rows(self, columns, data, cols):
        r = ''
        if data is None:
            data = []
        if columns:

            for row in data:
                r += '<tr>'
                for c in cols:
                    r += '<td>%s</td>' % self.eval_data(row.get(c, ''))
                for c in columns:
                    r += '<td>%s</td>' % self.eval_data(row.get(c, ''))
                r += '</tr>'
        else:
            for row in data:
                r += '<tr><td>%s</td></tr>' % row
        return r

    def eval_data(self, data):
        if data is None:
            data = ''
        cls = 'warning' if 'WARNING' in data else 'error' if 'ERROR' in data else None
        if cls is None:
            return data
        else:
            return '<span class="text-%s"> %s</span>' % (cls, data)

    def _table_header(self, columns, colums_default):
        header = ['<td>%s</td>' % data for data in columns]
        header = ''.join(header)
        return '<tr>%s%s</tr>' % (colums_default, header)

    def _html(self, filename, title, css_content, body):
        header = '<header><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>' + title + '</title><style>' + css_content + '</style></header>'

        html = '<html>%s<body>%s</body></html>' % (header, body)

        import codecs

        f = codecs.open(filename, 'w', 'utf-8')
        f.write(html)
        f.close()

    def in_table_format(self, data, columns):
        table_header = self._table_header(columns, '<td>id</td><td>label</td>')
        table_data = self._table_rows(columns, data, ['id', 'label'])
        return self._table_(table_header, table_data)


class CheckList(object):

    def __init__(self, pkg_name, default_validator_version=None, entities_table=None):
        self.pkg_name = pkg_name
        self.entities_table = entities_table
        self.default_validator_version = default_validator_version
        if default_validator_version:
            self.set_validator_version(default_validator_version)
        #dtd_filename, xsl_prep_report, xsl_report, xsl_preview, css_filename
        
    def set_validator_version(self, validator_version):
        self.selected_validator_version = validator_version
        if validator_version == '1.0':
            self.selected_validator_version = 'j1.0'
        version_data = _versions_.get(self.selected_validator_version, {}).get(self.pkg_name)
        self.xsl_report = version_data.get('xsl_report', None)
        self.xsl_prep_report = version_data.get('xsl_prep_report', None)
        self.xsl_preview = version_data.get('xsl_preview', None)
        self.dtd_filename = version_data.get('dtd', None)
        self.css_filename = 'file:///' + version_data.get('css', None)
        self.xsl_output = version_data.get('xsl_output', None)
        self.doctype = version_data.get('doctype', None)
        self._report = []
        
    def is_well_formed(self, xml_filename):
        xml = xml_is_well_formed(xml_filename)
        if xml is None:
            print('Converting entities...')
            f = open(xml_filename, 'r')
            content = f.read()
            f.close()

            content = convert_entities(content, self.entities_table)

            xml = xml_is_well_formed(content)
            if not xml is None:
                f = open(xml_filename, 'w')
                f.write(content)
                f.close()
        return xml

    def check_validator_version(self, xml):
        if self.default_validator_version is None:
            version = xml.find('.').attrib.get('dtd-version', '1.0')
            self.set_validator_version(version)

    def get_copy(self, xml_filename):
        temp_dir = tempfile.mkdtemp()
        temp_xml_filename = temp_dir + '/' + os.path.basename(xml_filename)
        shutil.copyfile(xml_filename, temp_xml_filename)
        return temp_xml_filename

    def dtd_validation(self, xml_filename, report_filename):
        if self.dtd_filename:
            f = open(xml_filename, 'r')
            content = f.read()
            f.close()

            xml_str = XMLStr(content)
            xml_str.fix_dtd_location(self.dtd_filename, self.doctype)

            if not content == xml_str.content:
                f = open(xml_filename, 'w')
                f.write(xml_str.content)
                f.close()

        return xml_validate(xml_filename, report_filename, True)

    def style_validation(self, xml_filename, style_checker_report):
        # STYLE CHECKER REPORT
        is_valid_style = False

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

                is_valid_style = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))
            else:
                is_valid_style = 'Unable to create validation report: ' + style_checker_report
        else:
            is_valid_style = 'Unable to generate xml for report: ' + xml_report

        return is_valid_style

    def output(self, xml_filename, xml_output):
        if os.path.exists(xml_output):
            os.unlink(xml_output)
        return xml_transform(xml_filename, self.xsl_output, xml_output)

    def check_list(self, xml_filename, pkg_files, img_path, xsl_param_new_name=''):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)
        xml = self.is_well_formed(xml_filename)
        pkg_files.checking_xml_filename = xml_filename

        if xml:
            pkg_files.is_well_formed = True

            self.check_validator_version(xml)

            temp_xml_filename = self.get_copy(xml_filename)
            pkg_files.is_valid_dtd = self.dtd_validation(temp_xml_filename, pkg_files.dtd_validation_report)
            pkg_files.is_valid_style = self.style_validation(temp_xml_filename, pkg_files.style_checker_report)
            if pkg_files.xml_output:
                self.output(temp_xml_filename, pkg_files.xml_output)

            os.unlink(temp_xml_filename)
            shutil.rmtree(os.path.dirname(temp_xml_filename))

        return pkg_files


class ContentValidation(object):

    def __init__(self, xml, filename):
        self.xml = xml
        self.issue_meta = {}
        self.article_meta = {}
        self.refs = []

        article_node = self.xml.find('.')
        journal_meta = self.xml.find('.//journal-meta')
        
        self.issue_meta['publisher-name'] = journal_meta.findtext('.//publisher-name')
        self.issue_meta['nlm-ta'] = journal_meta.findtext('.//journal-id[@journal-id-type="nlm-ta"]')
        self.issue_meta['eissn'] = journal_meta.findtext('.//issn[@pub-type="epub"]')

        self.issue_meta['pissn'] = journal_meta.findtext('.//issn[@pub-type="ppub"]')
        self.issue_meta['journal-title'] = journal_meta.findtext('.//journal-title')
        
        article_meta = self.xml.find('.//article-meta')

        self.issue_meta['issue'] = article_meta.findtext('.//issue')
        self.issue_meta['volume'] = article_meta.findtext('.//volume')

        for tp in ['ppub', 'epub', 'epub-ppub']:
            node = article_meta.find('.//pub-date[@pub-type="' + tp + '"]')
            if node is None:
                d = ['', '', '', '']
            else:
                d = []
                for elem in ['day', 'month', 'season', 'year']:
                    d.append(node.findtext(elem) if node.findtext(elem) else '')
            self.article_meta['date-' + tp] = '%s/%s%s/%s' % tuple(d)

        # ------
        self.article_meta['filename'] = filename
        self.article_meta['article-type'] = article_node.attrib.get('article-type', '')
        self.article_meta['lang'] = article_node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)

        self.article_meta['doi'] = article_meta.findtext('.//article-id[@pub-id-type="doi"]')
        self.article_meta['other id'] = article_meta.findtext('.//article-id[@pub-id-type="other"]')

        self.article_meta['subject'] = '|'.join([node.text for node in article_meta.findall('.//subject')])

        self.article_meta['fpage'] = article_meta.find('.//fpage').text
        self.article_meta['fpage_seq'] = article_meta.find('.//fpage').attrib.get('seq', '')

        self.article_meta['lpage'] = article_meta.find('.//lpage').text
        self.article_meta['lpage_seq'] = article_meta.find('.//lpage').attrib.get('seq', '')

        article_title = article_meta.find('.//article-title')
        self.article_meta['article-title'] = self._node_xml_content(article_title)
        
        self.article_meta['award-id'] = ','.join([award.text for award in article_meta.findall('.//award-id')])
        self.article_meta['ack'] = self._node_xml_content(self.xml.find('.//ack'))

        self.article_meta['license'] = self._node_xml(self.xml.find('.//license'))

        for tp in ['received', 'accepted']:
            node = self.xml.find('.//date[@date-type="' + tp + '"]')
            if node is not None:
                d = ''
                y = node.findtext('year')
                if y is None:
                    d += '0000'
                else:
                    d += y
                for item in [node.findtext('month'), node.findtext('day')]:
                    if item is None:
                        d += '00'
                    else:
                        item = '00' + item
                        d += item[-2:]
                self.article_meta[tp + ' date (history)'] = d
        
        self.article_meta['aff'] = []
        for aff in article_meta.findall('.//aff'):
            a = {'id': aff.attrib.get('id')}
            for item in ['orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3']:
                a[item] = aff.findtext('institution[@content-type="' + item + '"]')
            a['email'] = aff.findtext('email')
            a['country'] = aff.findtext('country')
            a['city'] = aff.findtext('addr-line/named-content[@content-type="city"]')
            a['state'] = aff.findtext('addr-line/named-content[@content-type="state"]')
            a['full'] = aff.text
            a['xml'] = etree.tostring(aff)
            self.article_meta['aff'].append(a)

        self.article_meta['abstract'] = self._node_xml_content(article_meta.find('.//abstract'))
        
        #self.article_meta['lang'] = article_title.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
        self.article_meta['trans-title'] = {}
        for trans_title in article_meta.findall('.//trans-title-group'):
            lang = trans_title.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
            self.article_meta['trans-title'][lang] = trans_title.findtext('trans-title')
        self.article_meta['trans-abstract'] = {}
        
        for trans_abstract in article_meta.findall('.//trans-abstract'):
            lang = trans_abstract.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
            self.article_meta['trans-abstract'][lang] = self._node_xml_content(trans_abstract)

        self.article_meta['kwd-group'] = {}
        for kwd_group in article_meta.findall('.//kwd-group'):
            lang = kwd_group.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', kwd_group.attrib.get('lang', '??'))
            self.article_meta['kwd-group'][lang] = [self._node_xml_content(kwd) for kwd in kwd_group.findall('kwd')]
        
        self.article_meta['author'] = []
        
        for author in article_meta.findall('.//contrib//name'):
            a = {}
            a['given-names'] = author.findtext('.//given-names')
            a['surname'] = author.findtext('.//surname')
            a['suffix'] = author.findtext('.//suffix')
            a['prefix'] = author.findtext('.//prefix')
            self.article_meta['author'].append(a)

        self.article_meta['collab'] = [node.text for node in article_meta.findall('.//contrib//collab')]

        self.article_meta['order'] = self._order(self.article_meta['fpage'], self.article_meta['fpage_seq'], self.article_meta['other id'])
        
        self.href = []
        for item in ['graphic', 'inline-graphic', 'media', 'inline-supplementary-material', 'supplementary-material']:
            for node in self.xml.findall('.//' + item):
                href = node.attrib.get('{http://www.w3.org/1999/xlink}href', None)
                if href:
                    self.href.append(href)
                else:
                    print(node.attrib)

        for ref in self.xml.findall('.//ref'):
            r = {}
            r['id'] = ref.attrib.get('id', None)

            e = ref.find('element-citation')
            r['type'] = e.attrib.get('publication-type')
            r['mixed'] = self._node_xml_content(ref.find('mixed-citation'))

            r['author'] = []
            
            for author in ref.findall('.//name'):
                a = {}
                a['given-names'] = author.findtext('.//given-names')
                a['surname'] = author.findtext('.//surname')
                a['suffix'] = author.findtext('.//suffix')
                a['prefix'] = author.findtext('.//prefix')
                r['author'].append(a)

            
            r['collab'] = [node.text for node in ref.findall('.//collab')]

            r['lang'] = None
            node = ref.find('.//article-title')
            if node is not None:
                r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
            else:
                node = ref.find('.//chapter-title')
                if node is not None:
                    r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
                else:
                    node = ref.find('.//source')
                    if node is not None:
                        r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)

            r['year'] = ref.findtext('.//year')
            r['source'] = ref.findtext('.//source')
            r['publisher-name'] = ref.findtext('.//publisher-name')
            r['publisher-loc'] = ref.findtext('.//publisher-loc')
            r['article-title'] = self._node_xml_content(ref.find('.//article-title'))
            r['chapter-title'] = self._node_xml_content(ref.find('.//chapter-title'))
            nodes = ref.findall('element-citation//ext-link')
            if nodes:
                r['ext-link'] = [uri.text for uri in nodes]
            
            nodes = ref.findall('element-citation//uri')
            if nodes:
                r['ext-link'] += [uri.text for uri in nodes]

            r['cited'] = ref.findtext('.//date-in-citation[@content-type="access-date"]')
            r['xml'] = etree.tostring(ref)
            self.refs.append(r)

    def _node_xml(self, node):
        if not node is None:
            return etree.tostring(node)

    def _node_xml_content(self, node):
        if not node is None:
            xml = etree.tostring(node)
            if xml[0:1] == '<':
                xml = xml[xml.find('>') + 1:]
                xml = xml[0:xml.rfind('</')]
            return xml
        return ''

    def _order(self, fpage, fpage_seq, other_id):
        if fpage.isdigit():
            order = int(fpage)
        else:
            order = 0
        if order == 0:
            if fpage_seq.isdigit():
                order = int(fpage_seq)
            else:
                order = 0
        if order == 0:
            if other_id.isdigit():
                order = int(other_id)
            else:
                order = 0
        return str(order)

    def _validate_data(self, data, expected):
        if isinstance(data, dict):
            result = []
            for key, item in expected.items():
                if not item == data.get(key, ''):
                    result.append('ERROR: Invalid value for %s. Expected: %s.' % (data.get(key, ''), item))
            return result
        elif isinstance(data, str):
            if not data == expected:
                result = 'ERROR: Invalid value for %s. Expected: %s.' % (data, expected)
            return result

    def _validate_presence_data(self, msg_type, status, data, label_list, scope=None):
        _scope = scope + ': ' if not scope is None else ''
        if isinstance(data, dict):
            result = []
            for req in label_list:
                at = '' if not data.get('id', None) else data['id'] + ': '
                if data.get(req, None) is None:
                    result.append(msg_type + ': ' + _scope + at + ' ' + status + ' ' + req)
                # if 'id' in data.keys():
                #     result['id'] = data['id']
                # if 'xml' in data.keys():
                #     result['xml'] = data['xml']

            #return result if not result == {} else None
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                result.append(self._validate_presence_data(msg_type, status, item, label_list, scope))
            result = [error for error in result if error]
            return result
        elif isinstance(data, str):
            if not data:
                return [msg_type + ': ' + _scope + ' ' + status + ' ' + label_list]
        else:
            if data is None:
                return [msg_type + ': ' + _scope + ' ' + status + ' ' + label_list]

    def _validate_conditional_required_data(self, data, required, scope=None):
        return self._validate_presence_data('WARNING', 'Required (if exists)', data, required, scope)

    def _validate_required_data(self, data, required, scope=None):
        return self._validate_presence_data('ERROR', 'Required', data, required, scope)

    def _validate_presence_of_at_least_one(self, data, labels):
        if not any([True for item in data if item]):
            return 'ERROR: Required one of ' + ' | '.join(labels)

    def _validate_previous_and_next(self, previous, next, labels, max_distance=None):
        if previous is None:
            previous = 0
        if next is None:
            next = 0
        if isinstance(previous, str):
            if previous.isdigit():
                previous = int(previous)
        if isinstance(next, str):
            if next.isdigit():
                next = int(next)

        if isinstance(previous, int) and isinstance(next, int):
            dist = next - previous
            if previous > next:
                return 'ERROR: %s %s must come before %s.' % (labels, previous, next)
            elif max_distance:
                if dist > max_distance:
                    return 'WARNING: Check %s: %s and %s.' % (labels, previous, next)

    def validations(self, expected_journal_meta, files):
        self.article_meta_validations = {}
        self.files_validations = ''
        self.issue_meta_validations = None
        self.refs_validations = []

        self.issue_meta_validations = self._validate_required_data(self.issue_meta, ['publisher-name', 'journal-title', 'issue'], 'journal-meta and issue-meta')
        self.issue_meta_validations += self._validate_conditional_required_data(self.issue_meta, ['issue'], 'journal-meta and issue-meta')
        if expected_journal_meta:
            self.issue_meta_validations += self._validate_data(self.issue_meta, expected_journal_meta)

        self.article_meta_validations['dates'] = self._validate_presence_of_at_least_one([self.article_meta.get('date-epub', ''), self.article_meta.get('date-ppub', ''), self.article_meta.get('date-epub-ppub', '')], ['epub date', 'ppub date', 'epub-ppub date'])

        self.article_meta_validations['issns'] = self._validate_presence_of_at_least_one([self.issue_meta['pissn'], self.issue_meta['eissn']], ['print issn', 'e-issn'])

        order = self.article_meta.get('order', '0')
        if order.isdigit():
            if 0 < int(order) < 100000:
                pass
            else:
                self.article_meta_validations['order'] = 'ERROR: Invalid value for order. It must be a number 1-9999'
        else:
            self.article_meta_validations['order'] = 'ERROR: Invalid value for order. It must be a number 1-9999'

        required_items = ['article-title', 'subject', 'doi', 'fpage', 'license']
        for label in required_items:
            self.article_meta_validations[label] = self._validate_required_data(self.article_meta.get(label, None), label)

        required_items = ['abstract', 'received date (history)', 'accepted date (history)']
        for label in required_items:
            self.article_meta_validations[label] = self._validate_conditional_required_data(self.article_meta.get(label, None), label)

        for trans_type in ['trans-abstract', 'trans-title', 'kwd-group']:
            translations = self.article_meta.get(trans_type, None)
            if translations:
                for lang, t in translations.items():
                    if lang == '??':
                        self.article_meta_validations[trans_type] = self._validate_conditional_required_data(None, trans_type + ' lang')
            else:
                self.article_meta_validations[trans_type] = self._validate_conditional_required_data(None, trans_type)
        
        self.article_meta_validations['pages'] = self._validate_previous_and_next(self.article_meta['fpage'], self.article_meta['lpage'], 'first page and last page', 20)

        self.article_meta_validations['history dates'] = self._validate_previous_and_next(self.article_meta.get('received', None), self.article_meta.get('accepted', None), 'received/accepted dates')

        #self.article_meta_validations['affs'] = self._validate_required_data(self.article_meta['aff'], ['orgname', 'city', 'state', 'country', 'full'])
        self.article_meta_validations['affs'] = self.validate_content(self.article_meta['aff'], ['orgname', 'full'], ['city', 'state', 'country'], [])
        self.article_meta_validations['author'] = self._validate_required_data(self.article_meta['author'], ['given-names', 'surname'])

        if not self.article_meta.get('award-id'):
            ack = self.article_meta.get('ack', None)
            if ack:
                # PARA IGNORAR <p id="parag28">
                if '<' in ack:
                    ack = ack.replace('<', '_BREAK_<')
                    ack = ack.split('_BREAK_')
                    new = ''
                    for item in ack:
                        if item.startswith('<'):
                            new += item[item.find('>'):]
                        else:
                            new += item
                    ack = new

                if '&#' in ack:
                    ack = ack.replace('&#', '_BREAK_&#')
                    ack = ack.split('_BREAK_')
                    new = ''
                    for item in ack:
                        if item.startswith('&#'):
                            new += item[item.find(';'):]
                        else:
                            new += item
                    ack = new

                if any([True for n in range(0, 10) if str(n) in ack]):
                    self.article_meta_validations['ack'] = 'WARNING: Check ack has contact number. %s' % self.article_meta.get('ack', None)
        count = len(self.refs)
        #print(count)
        self.article_meta_validations['ref-count'] = 'WARNING: Total of references = 0' if count == 0 else ''
        #print(self.article_meta_validations)
        for ref in self.refs:
            r = {}
            r = {'id': ref['id'], 'xml': ref['xml']}

            r['year-source'] = self._validate_required_data(ref, ['year', 'source', 'lang'])

            if not ref['type'] in ['journal', 'book', 'thesis', 'conf-proc', 'patent', 'report', 'software', 'web']:
                r['type'] = 'ERROR: Invalid value for element-citation/@publication-type: %s. Expected: %s.' % (ref['type'], ' | '.join(['journal', 'book', 'thesis', 'conf-proc', 'patent', 'report', 'software', 'web']))

            if not ref['mixed']:
                r['mixed'] = 'ERROR: Required mixed-citation'

            r['author'] = self._validate_required_data(ref['author'], ['given-names', 'surname'])

            r['authorship'] = self._validate_presence_of_at_least_one([ref.get('author', []), ref.get('collab', [])], ['author', 'collab'])
            if ref['type'] == 'book':
                r['publisher'] = self._validate_required_data(ref, ['publisher-name', 'publisher-loc'])
            if ref['type'] == 'web':
                r['link'] = self._validate_required_data(ref, ['ext-link', 'cited'])
            self.refs_validations.append(r)

        r_files = ['<li>' + f + '</li>' for f in self.href if not f in files]
        
        self.files_validations = 'ERROR: Required files <ul>%s</ul>' % ''.join(r_files) if len(r_files) > 0 else ''

    def validate_content(self, data, required_items, conditional_required_items, invalid_characteres, scope=None):
        results = []
        if required_items:
            results.append(self._validate_required_data(data, required_items, scope))
        if conditional_required_items:
            results.append(self._validate_conditional_required_data(data, conditional_required_items, scope))
        if invalid_characteres:
            results.append(self._has_invalid_characteres(data, invalid_characteres))
        return results

    def _has_invalid_characteres(self, content, invalid_characteres):
        if any([True for c in invalid_characteres if c in content]):
            return 'ERROR: Invalid characteres in %s (%s)' % (content, ' | '.join(invalid_characteres))


class ValidationResult(object):

    def __init__(self, pkg_path, report_path, xml_output_path=None, suffix='', preview_path=None):
        self.pkg_path = pkg_path
        self.report_path = report_path
        self.xml_output_path = xml_output_path
        self.preview_path = preview_path

        for d in [pkg_path, report_path, xml_output_path, preview_path]:
            if not d is None and not d == '':
                if not os.path.exists(d):
                    os.makedirs(d)

        self.suffix = suffix
        self.is_well_formed = False
        self.is_valid_style = False
        self.is_valid_dtd = False

    def name(self, curr_name, new_name):
        self.dtd_validation_report = self.report_path + '/' + curr_name + self.suffix + '.dtd.txt'
        self.style_checker_report = self.report_path + '/' + curr_name + self.suffix + '.rep.html'

        if self.preview_path == self.pkg_path:
            self.html_preview = self.pkg_path + '/' + new_name + '.html'
        elif not self.preview_path is None:
            self.html_preview = self.preview_path + '/' + curr_name + self.suffix + '.xml.html'
        else:
            self.html_preview = None

        if self.xml_output_path is None:
            self.xml_output = self.pkg_path + '/' + new_name + '.xml'
        else:
            self.xml_output = self.xml_output_path + '/' + new_name + '.xml'
        self.xml_name = curr_name
        self.new_name = new_name

    def manage_result(self, ctrl_filename):
        if ctrl_filename is None:
            if self.is_valid_dtd is True:
                os.unlink(self.dtd_validation_report)
            if self.is_valid_style is True:
                os.unlink(self.style_checker_report)
            if not self.is_well_formed:
                f = open(self.dtd_validation_report, 'a+')
                f.write('XML is not well formed')
                f.close()
        else:
            err_filename = ctrl_filename.replace('.ctrl', '.err')
            f = open(ctrl_filename, 'w')
            f.write('Finished')
            f.close()

            os.unlink(err_filename)
            f = open(err_filename, 'a+')
            if not self.is_well_formed:
                f.write(self.checking_xml_filename + ': XML is not well formed')

            elif not self.is_valid_dtd:
                if os.path.isfile(self.dtd_validation_report):
                    f.write(open(self.dtd_validation_report).read())
                else:
                    f.write('Unable to generate ' + self.dtd_validation_report)

            elif not self.is_valid_style:
                if not os.path.isfile(self.style_checker_report):
                    f.write('Unable to generate ' + self.style_checker_report)
            f.close()


class XPM(object):

    def __init__(self, sci_validator, pmc_validator, acron, default_version, entities_table):
        self.version_converter = _versions_.get(default_version, {}).get('sgm2xml')
        self.entities_table = entities_table
        self.acron = acron

        self.sci_validator = sci_validator
        self.pmc_validator = pmc_validator

    def matched_files(self, path, startswith):
        return [f for f in os.listdir(path) if f.startswith(startswith + '.') or f.startswith(startswith + '-')]

    def create_wrk_path(self, src_path, files, wrk_path):
        not_jpg = []
        if not os.path.exists(wrk_path):
            os.makedirs(wrk_path)
        for f in files:
            shutil.copyfile(src_path + '/' + f, wrk_path + '/' + f)
            r = self.img_to_jpg(src_path, f, wrk_path)
            if r:
                not_jpg.append(r)
        return not_jpg

    def img_to_jpg(self, src_path, filename, wrk_path):
        not_jpeg = None
        if filename.endswith('.tiff') or filename.endswith('.eps') or filename.endswith('.tif'):
            jpeg = filename[0:filename.rfind('.')] + '.jpg'

            if not jpeg in os.listdir(src_path):
                if IMG_CONVERTER:
                    if not img_to_jpeg(src_path + '/' + filename, wrk_path):
                        not_jpeg = src_path + '/' + filename
                else:
                    not_jpeg = src_path + '/' + filename
        return not_jpeg

    def add_renamed_files_to_packages(self, wrk_path, curr_name, new_name, package_paths):
        # copy <xml_file>.???
        for filename in os.listdir(wrk_path):
            if not filename.endswith('.jpg') and not filename.endswith('.sgm.xml'):
                new_filename = filename.replace(curr_name, new_name)
                for pkg_path in package_paths:
                    if not wrk_path + '/' + filename == pkg_path + '/' + new_filename:
                        shutil.copyfile(wrk_path + '/' + filename, pkg_path + '/' + new_filename)

    def add_href_files_to_packages(self, wrk_path, href_files_list, curr_name, new_name, scielo_pkg_path, pmc_pkg_path):
        missing_files = []
        #invalid_href = self._normalize_href_list()

        related_files = os.listdir(wrk_path)

        for href, suffix in href_files_list.items():
            matched_files = [f for f in related_files if f.startswith(href + '.')]
            for filename in matched_files:
                ext = filename[filename.rfind('.'):]

                matched = wrk_path + '/' + filename
                new_filename = curr_name + '-' + suffix + ext

                shutil.copyfile(matched, scielo_pkg_path + '/' + new_filename)
                if not filename.endswith('.jpg'):
                    shutil.copyfile(matched, pmc_pkg_path + '/' + new_filename)
            if not matched_files:
                missing_files.append(href)
        return missing_files

    def _normalize_href_list(self, href_files_list):
        invalid_href = []
        fixed = {}
        for href, suffix in href_files_list.items():
            ext = href[href.rfind('.'):]
            if ext in ['.tif', '.eps', '.tiff', '.jpg', '.pdf', '.html', '.htm'] or len(ext) == 4:
                invalid_href.append(href)
                href = href[0:href.find(ext)]
            fixed[href] = suffix
        href_files_list = fixed
        return (href_files_list, invalid_href)

    def normalize_xml(self, xml_filename, normalized_xml_path, err_filename, log_filename):
        """
        Normalize XML content
        """
        f = open(xml_filename)
        content = f.read()
        f.close()

        content, new_name, href_files_list, log = self._normalize_xml(content, xml_filename.endswith('.sgm.xml'), os.path.basename(xml_filename).replace('.sgm.xml', '').replace('.xml', ''))

        if xml_is_well_formed(content):
            f = open(normalized_xml_path + '/' + new_name + '.xml', 'w')
            f.write(content)
            f.close()

        log_message(log_filename, '\n'.join(log))
        return (new_name, href_files_list, log)

    def _normalize_xml(self, content, is_sgmxml, xml_name):
        """
        Normalize XML content
        """
        log = []
        # convert_ent_to_cha
        test = content
        content = convert_entities(content, self.entities_table)
        if not test == content:
            log.append('Convert entities.\n Done.')

        # fix problems of XML format
        if is_sgmxml:
            log.append('Fix SGML')
            xml_fix = XMLStr(content)
            xml_fix.fix()
            if not xml_fix.content == content:
                content = xml_fix.content
                log.append(' Done')

        # get href of images and new name
        new_name = xml_name
        href_files_list = {}

        if xml_is_well_formed(content):
            log.append('Metadata')
            new_name, href_files_list = XMLMetadata(content).new_names_and_embedded_files(self.acron, xml_name)
            log.append(' Done')
            if is_sgmxml:
                log.append('SGML to XML')
                content = xml_content_transform(content, self.version_converter)
                log.append(' Done')
        else:
            log.append('XML is not well formed')
        return (content, new_name, href_files_list, log)

    def validate_packages(self, xml_name, new_name, scielo_validation_result, pmc_validation_result, err_filename, ctrl_filename):
        xsl_new_name = new_name if new_name != xml_name else ''
        img_path = scielo_validation_result.pkg_path

        if os.path.isfile(scielo_validation_result.pkg_path + '/' + new_name + '.xml'):
            scielo_validation_result = self.sci_validator.check_list(scielo_validation_result.pkg_path + '/' + new_name + '.xml', scielo_validation_result, img_path)
            scielo_validation_result.manage_result(ctrl_filename)

            if os.path.exists(pmc_validation_result.pkg_path + '/' + new_name + '.xml'):
                pmc_validation_result = self.pmc_validator.check_list(pmc_validation_result.pkg_path + '/' + new_name + '.xml', pmc_validation_result, img_path, xsl_new_name)

                if ctrl_filename is None:
                    pmc_validation_result.manage_result(None)

                if os.path.exists(pmc_validation_result.xml_output):
                    print('  Finished')
                else:
                    print('\nUnable to create ' + pmc_validation_result.xml_output)
                    f = open(err_filename, 'a+')
                    f.write('\nUnable to create ' + pmc_validation_result.xml_output)
                    f.close()
            else:
                print('Unable to create ' + pmc_validation_result.pkg_path + '/' + new_name + '.xml')

                f = open(err_filename, 'a+')
                f.write('\nUnable to create ' + pmc_validation_result.pkg_path + '/' + new_name + '.xml')
                f.close()
        else:
            f = open(err_filename, 'a+')
            f.write('\nUnable to find ' + scielo_validation_result.pkg_path + '/' + new_name + '.xml')
            f.close()

    def make_article_packages(self, wrk_path, curr_name, new_name, href_files_list, scielo_pkg_path, pmc_pkg_path, err_filename, log_filename):
        
        log_message(log_filename, scielo_pkg_path + '/' + new_name + '.xml')

        if os.path.exists(scielo_pkg_path + '/' + new_name + '.xml'):
            log_message(log_filename, '_normalize_href_list')

            href_files_list, invalid_href = self._normalize_href_list(href_files_list)

            log_errors(err_filename, 'Invalid href, which must not have extension', invalid_href)

            package_paths = [scielo_pkg_path, pmc_pkg_path]

            log_message(log_filename, 'add_renamed_files_to_packages')
            self.add_renamed_files_to_packages(wrk_path, curr_name, new_name, package_paths)
            
            log_message(log_filename, 'add_href_files_to_packages')

            expected_files = self.add_href_files_to_packages(wrk_path, href_files_list, curr_name, new_name, scielo_pkg_path, pmc_pkg_path)

            log_errors(err_filename, 'Required files', expected_files)
        return (os.path.isfile(pmc_pkg_path + '/' + new_name + '.xml'))

    def make_packages(self, xml_filename, ctrl_filename, xml_path, work_path, scielo_val_res, pmc_val_res, err_filename):

        files = [xml_filename] if xml_filename else [f for f in os.listdir(xml_path) if f.endswith('.xml')]

        report_path = scielo_val_res.report_path

        for xml_filename in files:
            print('\n== %s ==\n' % xml_filename)

            xml_name = xml_filename.replace('.sgm.xml', '').replace('.xml', '')
            matched_files = self.matched_files(xml_path, xml_name)

            wrk_path = work_path + '/' + xml_name

            log_filename = scielo_val_res.report_path + '/' + xml_name + '.log'
            err_filename = scielo_val_res.report_path + '/' + xml_name + '.err.txt'

            not_jpg = self.create_wrk_path(xml_path, matched_files, wrk_path)

            log_errors(err_filename, 'JPG were not converted', not_jpg)

            new_name, href_files_list, log = self.normalize_xml(wrk_path + '/' + xml_filename, scielo_val_res.pkg_path, err_filename, log_filename)

            if os.path.exists(scielo_val_res.pkg_path + '/' + new_name + '.xml'):
                if self.make_article_packages(wrk_path, xml_name, new_name, href_files_list, scielo_val_res.pkg_path, pmc_val_res.pkg_path, err_filename, log_filename):

                    scielo_val_res.name(xml_name, new_name)
                    pmc_val_res.name(xml_name, new_name)

                    self.validate_packages(xml_name, new_name, scielo_val_res, pmc_val_res, err_filename, ctrl_filename)
                else:
                    log.append('Unable to generate the packages')
            else:
                log.append('Unable to normalize XML')
            #log_message(log_filename, '\n'.join(log))


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

        if not os.path.exists(report_path):
            os.makedirs(report_path)

        err_filename = report_path + '/errors.txt'

        sci_val_res = ValidationResult(scielo_pkg_path, report_path, pmc_pkg_path, '', None)
        pmc_val_res = ValidationResult(pmc_pkg_path, report_path, None, '', None)

        sci_validator = CheckList('scielo', version, entities_table)
        pmc_validator = CheckList('pmc', version)

        xml_pkg_mker = XPM(sci_validator, pmc_validator, acron, version, entities_table)
        xml_pkg_mker.make_packages(xml_filename, ctrl_filename, xml_path, wrk_path, sci_val_res, pmc_val_res, err_filename)

        report = PkgReport(scielo_pkg_path, report_path)
        #report.generate_articles_report(ctrl_filename is not None)
        report.generate_articles_report(True)
        report.generate_lists()

        print('\n=======')
        print('\nGenerated packages in:\n' + '\n'.join([scielo_pkg_path, pmc_pkg_path, ]))
        for report_path in list(set([report_path, report_path, ])):
            if os.listdir(report_path):
                print('\nReports in: ' + report_path)
        print('\n==== END ===\n')

    else:
        print(task)

###
_versions_ = configure_versions_location()
entities_table = EntitiesTable(ENTITIES_TABLE_FILENAME)
