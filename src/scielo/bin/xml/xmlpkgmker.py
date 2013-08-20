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

# global variables
THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))

CONFIG_JAVA_PATH = 'java'
CONFIG_JAR_PATH = THIS_LOCATION + '/../jar'
CONFIG_ENT_TABLE_PATH = THIS_LOCATION
CONFIG_VERSIONS_PATH = THIS_LOCATION + '/../pmc'


JAVA_PATH = CONFIG_JAVA_PATH
JAR_TRANSFORM = CONFIG_JAR_PATH + '/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = CONFIG_JAR_PATH + '/XMLCheck.jar'
ENTITIES_TABLE_FILENAME = CONFIG_ENT_TABLE_PATH + '/reuse/encoding/entities'


def configure_versions_location():
    PMC_PATH = CONFIG_VERSIONS_PATH
    version_configuration = {}
    version_configuration['3.0'] = {}
    version_configuration['3.0']['sgm2xml'] = PMC_PATH + '/v3.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['3.0']['scielo'] = {}
    version_configuration['3.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['scielo']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['scielo']['css'] = PMC_PATH + '/v3.0/xsl/previewers/scielo.css'
    version_configuration['3.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['3.0']['scielo']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['scielo']['xsl_preview'] = PMC_PATH + '/v3.0/xsl/previewers/scielo-html.xsl'
    version_configuration['3.0']['scielo']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['3.0']['pmc'] = {}
    version_configuration['3.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['pmc']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['pmc']['css'] = PMC_PATH + '/v3.0/xsl/jpub/jpub-preview.css'
    version_configuration['3.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
    version_configuration['3.0']['pmc']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['pmc']['xsl_preview'] = [PMC_PATH + '/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
    version_configuration['3.0']['pmc']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/pmc.xsl'

    version_configuration['j1.0'] = {}
    version_configuration['j1.0']['sgm2xml'] = PMC_PATH + '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['j1.0']['scielo'] = {}
    version_configuration['j1.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'

    version_configuration['j1.0']['scielo']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['scielo']['css'] = PMC_PATH + '/j1.0/xsl/previewers/scielo.css'
    version_configuration['j1.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['j1.0']['scielo']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['scielo']['xsl_preview'] = PMC_PATH + '/j1.0/xsl/previewers/scielo-html.xsl'
    version_configuration['j1.0']['scielo']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['j1.0']['pmc'] = {}
    version_configuration['j1.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
    version_configuration['j1.0']['pmc']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['pmc']['css'] = version_configuration['3.0']['pmc']['css']
    version_configuration['j1.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/nlm-stylechecker.xsl'
    version_configuration['j1.0']['pmc']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['pmc']['xsl_preview'] = version_configuration['3.0']['pmc']['xsl_preview']
    version_configuration['j1.0']['pmc']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/pmc.xsl'
    return version_configuration


###
def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
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

                if self.is_valid_char(char) and self.is_valid_named(named_ent):
                    #entity_char = named_ent.replace('&','').replace(';','')
                    if self.table_number2char.get(number_ent, None) is None:
                        self.table_number2char[number_ent] = char
                    if self.table_named2char.get(named_ent, None) is None:
                        self.table_number2char[named_ent] = char

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

    not_found = []
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
                content = h.unescape(content)
            except:
                print('Unable to use h.unescape')

        if '&' in content:
            if entities_table:
                while '&' in content:
                    ent = content[content.find('&'):]
                    ent = ent[0:ent.find(';')+1]

                    char = entities_table.ent2chr(ent)
                    if char == ent:
                        content = content.replace(ent, ent.replace('&', PREFIX_ENT))
                        not_found.append(ent)
                    else:
                        content = content.replace(ent, char)

        content = content.replace(PREFIX_ENT, '&')
    if not_found:
        f = open('unknown_ent.txt', 'a+')
        f.write('\n'.join(not_found))
        f.close()
    return content


### IMAGES
def img_to_jpeg(image_filename, jpg_path, replace=False):
    if image_filename.endswith('.tiff') or image_filename.endswith('.eps') or image_filename.endswith('.tif'):
        image_name = os.path.basename(image_filename)
        jpg_filename = jpg_path + '/' + image_name[0:image_name.rfind('.')] + '.jpg'

        if not os.path.exists(jpg_filename) or replace:
            try:
                im = Image.open(image_filename)
                im.thumbnail(im.size)
                im.save(jpg_filename, "JPEG")
            except Exception as inst:
                print(inst)

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
                    s += str(n) + ':' + line + '\n'
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
    if content[0:1] == '<':
        return etree.parse(StringIO(content))
    else:
        return etree.parse(content)


def xml_content_transform(content, xsl_filename):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(content)
    f.close()

    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.close()

    if xml_transform(f.name, xsl_filename, f2.name):
        fp = open(f2.name, 'r')
        content = fp.read()
        fp.close()
        os.unlink(f2.name)
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
    #print(cmd)
    os.system(cmd)

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
            content = self._fix_style_tags(content)
            if not xml_is_well_formed(content):
                content = self._fix_open_close(content)
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
    def __init__(self, pkg_path, report_path, suffix=''):
        self.pkg_path = pkg_path
        self.suffix = suffix
        self.report_path = report_path
        if not os.path.exists(pkg_path):
            os.makedirs(pkg_path)
        if not os.path.exists(report_path):
            os.makedirs(report_path)

    def name(self, curr_name, new_name):
        self.dtd_validation_report = self.report_path + '/' + curr_name + self.suffix + '.dtd.txt'
        self.style_checker_report = self.report_path + '/' + curr_name + self.suffix + '.rep.html'
        self.html_preview = self.report_path + '/' + curr_name + self.suffix + '.xml.html'
        self.xml_output = self.pkg_path + '/' + new_name + '.xml'


class XMLValidations:
    def __init__(self, pkg_name, entities_table=None):
        self.pkg_name = pkg_name
        self.entities_table = entities_table
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
        self.css_filename = version_data.get('css', None)
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
        return report_ok

    def _preview(self, xml_filename, html_preview, xsl_param_img_path, xsl_param_new_name=''):
        preview_ok = False
        if os.path.exists(html_preview):
            os.unlink(html_preview)
        xsl_params = {'path_img': xsl_param_img_path + '/', 'css':  self.css_filename, 'new_name': xsl_param_new_name}
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
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)

        err_files = []
        f = open(xml_filename, 'r')
        content = f.read()
        f.close()

        xml = xml_is_well_formed(content)
        if not xml:
            content = convert_ent_to_char(content, self.entities_table)
            xml = xml_is_well_formed(content)
            if xml:
                f = open(xml_filename, 'w')
                f.write(content)
                f.close()

        if xml:
            dtd_version = xml.find('.').attrib.get('dtd-version', '1.0')
            self.select_version(dtd_version)

            temp_dir = tempfile.mkdtemp()
            temp_xml_filename = temp_dir + '/' + os.path.basename(xml_filename)
            shutil.copyfile(xml_filename, temp_xml_filename)

            if self.dtd_filename:
                content = XMLFixer().fix_dtd_location(content, self.dtd_filename, self.doctype)
                f = open(temp_xml_filename, 'w')
                f.write(content)
                f.close()

            if os.path.exists(temp_xml_filename):
                is_dtd_valid = xml_validate(temp_xml_filename, pkg_files.dtd_validation_report, True)

                if not is_dtd_valid:
                    err_files.append(pkg_files.dtd_validation_report.replace('.dtd.txt', '.err.txt'))
                    shutil.move(pkg_files.dtd_validation_report, pkg_files.dtd_validation_report.replace('.dtd.txt', '.err.txt'))

                # STYLE CHECKER REPORT
                if not self._style_checker_report(temp_xml_filename, pkg_files.style_checker_report):
                    err_files.append(pkg_files.style_checker_report.replace('.rep.html', '.rep.err.html'))
                    shutil.move(pkg_files.style_checker_report, pkg_files.style_checker_report.replace('.rep.html', '.rep.err.html'))

                # PREVIEW
                if pkg_files.html_preview:
                    self._preview(temp_xml_filename, pkg_files.html_preview, img_path, xsl_param_new_name)

                if pkg_files.xml_output:
                    self._output(temp_xml_filename, pkg_files.xml_output)

                os.unlink(temp_xml_filename)
                shutil.rmtree(temp_dir)
        else:
            # not well formed
            err_files.append(xml_filename)
            shutil.copyfile(xml_filename, pkg_files.report_path + '/' + os.path.basename(xml_filename) + '.err.txt')

        return err_files


class XMLMetadata:
    def __init__(self, content):
        self.root = etree.parse(StringIO(content))

    def _meta_xml(self, node):
        issn, volid, issueno, suppl, fpage, order = ['', '', '', '', '', '']
        issn = self.root.findtext('.//front/journal-meta/issn[1]')
        volid = node.findtext('./volume')
        issueno = node.findtext('./issue')
        suppl = node.findtext('./supplement')
        supplnum = ''
        supplvol = ''
        if not suppl and 'sup' in issueno.lower():
            n = issueno.strip().split()
            if len(n) == 3:
                # <issue>n suppl s</issue>
                issueno = n[0]
                supplnum = n[2]
            elif len(n) == 2:

                if 'sup' in n[0]:
                    # <issue>suppl s</issue>
                    issueno = ''
                    supplvol = n[1]
                else:
                    # <issue>n suppl</issue>
                    issueno = n[0]
                    supplnum = '0'
            elif len(n) == 1:
                # <issue>suppl</issue>
                supplvol = '0'
        if supplnum:
            suppl = supplnum
        elif supplvol:
            suppl = supplvol
        else:
            suppl = ''

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
                attribs = self.root.attrib
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
                page_or_order = '00000' + fpage + seq
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
        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href']

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
                    for attrib_name in test_href:
                        href = graphic_node.attrib.get(attrib_name)
                        if href:
                            r[href] = id
                            break
        return r

    def new_name_and_img_list(self, acron, alternative_id=''):
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        xml_images_list = self.xml_data_image_names()
        return (new_name, xml_images_list)


class XMLPkgMker:

    def __init__(self, src, scielo_pkg_files, pmc_pkg_files, acron, version_converter, entities_table=None):
        if os.path.isfile(src) and src.endswith('.xml'):
            self.src_path = os.path.dirname(src)
            self.xml_filename = os.path.basename(src)
            self.xml_name = self.xml_filename.replace('.sgm.xml', '').replace('.xml', '')
        else:
            self.src_path = src
            self.xml_filename = None
            self.xml_name = None
        self.entities_table = entities_table
        self.scielo_pkg_files = scielo_pkg_files
        self.pmc_pkg_files = pmc_pkg_files

        self.acron = acron
        self.version_converter = version_converter
        #_versions_[self.version]['sgm2xml']

        self.src_copy_path = tempfile.mkdtemp()
        self.new_name_path = tempfile.mkdtemp()

        self.sci_validations = XMLValidations('scielo', self.entities_table)
        self.pmc_validations = XMLValidations('pmc')

    def _normalize_xml(self, input_filename, alternative_id):
        """
        Normalize XML content
        """
        f = open(input_filename, 'r')
        content = f.read()
        f.close()

        # convert_ent_to_char
        content = convert_ent_to_char(content, self.entities_table)

        # fix problems of XML format
        if input_filename.endswith('.sgm.xml'):
            content = XMLFixer().fix(content)

        # get href of images and new name
        new_name, img_list = XMLMetadata(content).new_name_and_img_list(self.acron, alternative_id)

        if input_filename.endswith('.sgm.xml'):
            content = xml_content_transform(content, self.version_converter)

        f = open(self.new_name_path + '/' + new_name + '.xml', 'w')
        f.write(content)
        #error_messages.append('Unable to create ' + xml_filename)
        f.close()

        return [new_name, img_list]

    def _create_src_copy(self, selected_files):
        for filename in selected_files:
            shutil.copyfile(self.src_path + '/' + filename, self.src_copy_path + '/' + filename)
            if IMG_CONVERTER:
                if (filename.endswith('.tiff') or filename.endswith('.eps') or filename.endswith('.tif')):
                    img_to_jpeg(self.src_path + '/' + filename, self.src_copy_path)

    def _add_related_files_to_packages(self, related_files, curr_name, new_name):
        # copy <xml_file>.???
        for filename in [f for f in related_files if f.startswith(curr_name + '.')]:
            related_file = self.src_copy_path + '/' + filename
            new_filename = filename.replace(curr_name, new_name)
            shutil.copyfile(related_file, self.scielo_pkg_files.pkg_path + '/' + new_filename)
            shutil.copyfile(related_file, self.pmc_pkg_files.pkg_path + '/' + new_filename)

    def _add_img_to_packages(self, related_files, img_list, new_name):
        # copy image files which starts with <href>.
        for href, suffix in img_list.items():
            for image_filename in [f for f in related_files if f.startswith(href + '.')]:
                ext = image_filename[image_filename.rfind('.'):]

                img_filename = self.src_copy_path + '/' + image_filename
                new_filename = new_name + '-' + suffix + ext

                #shutil.copyfile(img_filename, self.new_name_path + '/' + new_filename)
                shutil.copyfile(img_filename, self.scielo_pkg_files.pkg_path + '/' + new_filename)
                if not image_filename.endswith('.jpg'):
                    shutil.copyfile(img_filename, self.pmc_pkg_files.pkg_path + '/' + new_filename)

    def _make_packages_for_one_file(self, xml_file, curr_name, related_files):
        reports = []
        new_name, img_list = self._normalize_xml(self.src_copy_path + '/' + xml_file, curr_name)
        xml_filename = self.new_name_path + '/' + new_name + '.xml'

        self.scielo_pkg_files.name(curr_name, new_name)
        self.pmc_pkg_files.name(curr_name, new_name)
        xsl_new_name = new_name if new_name != curr_name else ''

        if os.path.exists(xml_filename):
            self._add_related_files_to_packages(related_files, curr_name, new_name)
            self._add_img_to_packages(related_files, img_list, new_name)

            img_path = self.scielo_pkg_files.pkg_path

            reports = self.sci_validations.check_list(xml_filename, self.scielo_pkg_files, img_path)

            if os.path.exists(self.scielo_pkg_files.xml_output):
                #dtd_validation_report = self.report_path + '/' + curr_name + '.err.txt'
                xml_filename = self.scielo_pkg_files.xml_output

                reports += self.pmc_validations.check_list(xml_filename, self.pmc_pkg_files, img_path, xsl_new_name)
                if not os.path.exists(self.pmc_pkg_files.xml_output):
                    f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
                    f.write('\nUnable to create ' + self.scielo_pkg_files.xml_output)
                    f.close()
            else:
                f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
                f.write('\nUnable to create ' + self.scielo_pkg_files.xml_output)
                f.close()
        else:
            f = open(self.scielo_pkg_files.dtd_validation_report, 'a+')
            f.write('Unable to create ' + xml_filename)
            f.close()
        if os.path.exists(self.scielo_pkg_files.dtd_validation_report) and not self.scielo_pkg_files.dtd_validation_report in reports:
            reports.append(self.scielo_pkg_files.dtd_validation_report)

        return reports

    def make_packages(self):
        if self.xml_filename:
            # only one file
            selected_files = [f for f in os.listdir(self.src_path) if f.startswith(self.xml_name)]
        else:
            selected_files = [f for f in os.listdir(self.src_path) if os.path.isfile(self.src_path + '/' + f)] 
            #self._clean_folders()

        self._create_src_copy(selected_files)

        xml_files = [f for f in selected_files if f.endswith('.xml')]
        non_xml_files = [f for f in selected_files if not f.endswith('.xml')]

        err_files = []
        for xml_file in xml_files:
            curr_name = xml_file.replace('.xml', '').replace('.sgm.xml', '')
            related_files = [f for f in non_xml_files if f.startswith(curr_name)]
            #xml_file, selected_files_path, normalized_pck_path, curr_name, related_files

            reports = self._make_packages_for_one_file(xml_file, curr_name, related_files)

            if reports:
                print('Generated reports:\n' + '\n'.join(reports))
                err_files += reports

        print('Generated packages in:\n' + '\n'.join([self.scielo_pkg_files.pkg_path, self.pmc_pkg_files.pkg_path, ]))

        shutil.rmtree(self.src_copy_path)
        shutil.rmtree(self.new_name_path)


def make_packages(src, acron, version='j1.0'):
    if not version in _versions_.keys():
        version = 'j1.0'
    doit = False
    from datetime import datetime
    now = datetime.now().isoformat().replace(':', '_').replace('T', '_')
    now = now[0:now.find('.')]
    if src.endswith('.sgm.xml'):
        # src = serial/acron/issue/pmc/pmc_work/article/file.sgm.xml
        sgmxml_filename = src
        sgmxml_path = os.path.dirname(src)
        pmc_path = os.path.dirname(os.path.dirname(sgmxml_path))
        acron = os.path.basename(os.path.dirname(os.path.dirname(pmc_path)))

        if os.path.exists(pmc_path + '/pmc_src'):
            pmc_src = pmc_path + '/pmc_src'
        elif os.path.exists(pmc_path + '/src'):
            pmc_src = pmc_path + '/src'
        shutil.copyfile(sgmxml_filename, pmc_src + '/' + os.path.basename(sgmxml_filename))
        scielo_pkg_path = pmc_path + '/xml_package'
        pmc_pkg_path = pmc_path + '/pmc_package'
        report_path = pmc_path + '/reports'
        doit = True
    elif src.endswith('.xml') and os.path.isfile(src):
        path = os.path.dirname(src) + '_' + now
        scielo_pkg_path = path + '/scielo_package'
        pmc_pkg_path = path + '/pmc_package'
        report_path = path + '/reports'
        doit = True
    elif os.path.isdir(src) and any([True for f in os.listdir(src) if f.endswith('.xml')]):
        path = src + '_' + now
        scielo_pkg_path = path + '/scielo_package'
        pmc_pkg_path = path + '/pmc_package'
        report_path = path + '/reports'
        doit = True
    if doit:
        scielo_pkg_files = ValidationFiles(scielo_pkg_path, report_path)
        pmc_pkg_files = ValidationFiles(pmc_pkg_path, report_path, '.pmc')
        xml_pkg_mker = XMLPkgMker(src, scielo_pkg_files, pmc_pkg_files, acron, _versions_.get(version, {}).get('sgml2xml'), entities_table)
        xml_pkg_mker.make_packages()


###
_versions_ = configure_versions_location()
entities_table = EntitiesTable(ENTITIES_TABLE_FILENAME)
