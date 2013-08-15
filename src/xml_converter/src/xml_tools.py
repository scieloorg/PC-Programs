import random
import os
import shutil

from StringIO import StringIO
import xml.etree.ElementTree as etree

java_path = 'java'
jar_validate = '/saxonb9-1-0-8j/saxon9.jar'
jar_transform = '/XMLCheck.jar'

_versions_ = {}

_versions_['3.0'] = {}
_versions_['3.0']['sgm2xml'] = '/v3.0/xsl/sgml2xml/sgml2xml.xsl'

_versions_['3.0']['scielo'] = {}
_versions_['3.0']['scielo']['dtd'] = None
_versions_['3.0']['scielo']['css'] = '/v3.0/xsl/previewers/scielo.css'
_versions_['3.0']['scielo']['xsl_prep_report'] = '/v3.0/scielo-style/stylechecker.xsl'
_versions_['3.0']['scielo']['xsl_report'] = '/v3.0/nlm-style-4.6.6/style-reporter.xsl'
_versions_['3.0']['scielo']['xsl_preview'] = '/v3.0/previewers/scielo-html.xsl'
_versions_['3.0']['scielo']['xsl_output'] = '/v3.0/sgml2xml/xml2pmc.xsl'

_versions_['3.0']['pmc'] = {}
_versions_['3.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
_versions_['3.0']['pmc']['dtd'] = '/v3.0/dtd/journalpublishing3.dtd'
_versions_['3.0']['pmc']['css'] = '/v3.0/xsl/jpub/jpub-preview.css'
_versions_['3.0']['pmc']['xsl_prep_report'] = '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
_versions_['3.0']['pmc']['xsl_report'] = '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
_versions_['3.0']['pmc']['xsl_preview'] = ['/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
_versions_['3.0']['pmc']['xsl_output'] = '/v3.0/xsl/sgml2xml/pmc.xsl'

_versions_['j1.0'] = {}
_versions_['j1.0']['sgm2xml'] = '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

_versions_['j1.0']['scielo'] = {}

_versions_['j1.0']['scielo']['dtd'] = None
_versions_['j1.0']['scielo']['css'] = '/j1.0/xsl/previewers/scielo.css'
_versions_['j1.0']['scielo']['xsl_prep_report'] = '/j1.0/scielo-style/stylechecker.xsl'
_versions_['j1.0']['scielo']['xsl_report'] = '/j1.0/nlm-style-5.2/style-reporter.xsl'
_versions_['j1.0']['scielo']['xsl_preview'] = '/j1.0/previewers/scielo-html.xsl'
_versions_['j1.0']['scielo']['xsl_output'] = '/j1.0/sgml2xml/xml2pmc.xsl'

_versions_['j1.0']['pmc'] = {}
_versions_['j1.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
_versions_['j1.0']['pmc']['dtd'] = '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
_versions_['j1.0']['pmc']['css'] = _versions_['3.0']['pmc']['css']
_versions_['j1.0']['pmc']['xsl_prep_report'] = '/j1.0/xsl/nlm-style-5.2/nlm-stylechecker.xsl'
_versions_['j1.0']['pmc']['xsl_report'] = '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
_versions_['j1.0']['pmc']['xsl_preview'] = _versions_['3.0']['pmc']['xsl_preview']
_versions_['j1.0']['pmc']['xsl_output'] = '/j1.0/xsl/sgml2xml/pmc.xsl'


def img_to_jpeg(img_path, jpg_path, replace=False):
    r = False
    failures = []
    try:
        import Image

        files = [f for f in os.listdir(img_path) if not f.endswith('.jpg')]
        for f in files:
            jpg_filename = jpg_path + '/' + f[0:f.rfind('.')] + '.jpg'
            image_filename = img_path + '/' + f
            if replace or not os.path.exists(jpg_filename):
                try:
                    im = Image.open(image_filename)
                    im.thumbnail(im.size)
                    im.save(jpg_filename, "JPEG")
                except Exception, e:
                    print e
                    print jpg_filename
                    failures.append(image_filename)
        ok = len(files)-len(failures)

        print('Converted ' + str(ok) + '/' + str(len(files)))
        r = len(files) == ok
    except:
        print('Desirable have installed PIL in order to convert images to jpg')
    return r


class EntitiesTable:
    def __init__(self, filename='entities'):
        lines = read_file(filename)

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

entities_table = EntitiesTable(os.path.dirname(os.path.realpath(__file__)) + '/reuse/encoding/entities')


def normalize_entities(content):
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
            #PREFIX_ENT = '#PREFIX_ENT#'
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


def xml_validate(xml_filename, result_filename, dtd_validation=False):
    validation_type = ''

    if dtd_validation:
        validation_type = '--validate'

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)

    cmd = java_path + ' -cp ' + jar_validate + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' + validation_type + '>' + temp_result_filename

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
    import xml.etree.ElementTree as etree
    from StringIO import StringIO

    if content[0:1] == '<':
        return etree.parse(StringIO(content))
    else:
        return etree.parse(content)


def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if ' ' in v:
            r += k + '=' + '"' + v + '" '
        else:
            r += k + '=' + v + ' '
    return r


def xml_content_transform(content, xsl_filename):
    import tempfile
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

    cmd = java_path + ' -jar ' + jar_transform + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)

    os.system(cmd)

    if not os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        error = True

    shutil.move(temp_result_filename, result_filename)

    return (not error)


def tranform_in_steps(xml_filename, xsl_list, result_filename, parameters={}):
    input_filename = xml_filename + '.in'
    output_filename = xml_filename + '.out'
    error = False

    shutil.copyfile(xml_filename, input_filename)
    if os.path.exists(result_filename):
        os.unlink(result_filename)

    for xsl in xsl_list:
        r = xml_transform(input_filename, xsl, output_filename, parameters)
        if r:
            shutil.copyfile(output_filename, input_filename)
        else:
            error = True
            break

    if os.path.exists(input_filename):
        os.unlink(input_filename)
    shutil.move(output_filename, result_filename)
    return not error


class XMLFixer:

    def __init__(self, default_dtd_version, xml_filename):
        self.xml_filename = xml_filename
        f = open(xml_filename, 'r')
        self.content = f.read()
        f.close()
        self.default_dtd_version = default_dtd_version

    def _fix_dtd_location(self, dtd_filename):
        if not dtd_filename in self.content:
            if not '<?xml ' in self.content:
                self.content = '<?xml version="1.0" encoding="utf-8"?>\n' + self.content

            if ' dtd-version="' in self.content:
                dtd_version = self.content[self.content.find(' dtd-version="')+len(' dtd-version="'):]
                dtd_version = dtd_version[0:dtd_version.find('"')]
            else:
                dtd_version = self.default_dtd_version

            if '<!DOCTYPE' in self.content:
                doctype = self.content[self.content.find('<!DOCTYPE'):]
                doctype = self.content[0:doctype.find('>')+1]
                self.content = self.content.replace(doctype, '')

            if not '<!DOCTYPE' in self.content:
                self.content = self.content.replace('<article ', self._doctypes[dtd_version].replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')

    def _fix_entities(self):
        pass

    def _fix_tags(self):
        pass


class SGMLXML:
    def __init__(self):
        pass

    def fix(self, content):
        ok = xml_is_well_formed(content)
        if not ok:
            content = self._fix_style_tags(content)

            ok = xml_is_well_formed(content)
            if not ok:
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


class ValidationIO:
    def __init__(self, src_xml_filename, work_path, dtd_validation_report, style_checker_report, html_preview='', output_filename='', img_path=''
        , new_name=''):
        self.src_xml_filename = src_xml_filename
        self.work_path = work_path
        self.dtd_validation_report = dtd_validation_report
        self.html_report = style_checker_report
        self.html_preview = html_preview

        self.img_path = 'file:///' + img_path if ':' in img_path else img_path
        self.new_name = new_name

        basename = os.path.basename(self.src_xml_filename)
        filename = self.basename.replace('.xml', '')

        self.work_path += '/' + filename
        self.xml_filename = self.work_path + '/' + basename

        if os.path.exists(self.work_path):
            for f in os.listdir(self.work_path):
                os.unlink(self.work_path + '/' + f)
        else:
            os.makedirs(self.work_path)
        shutil.copyfile(self.src_xml_filename, self.xml_filename)

        self.result_filenames = [dtd_validation_report, style_checker_report, html_preview, output_filename]
        self.result_filenames = [f for f in self.result_filenames if f != '']
        for f in self.result_filenames:
            if os.path.exists(f):
                os.unlink(f)


class XMLValidations:
    def __init__(self, version):
        #dtd_filename, xsl_prep_report, xsl_report, xsl_preview, css_filename
        self.xsl_report = version.get('xsl_report', None)
        self.xsl_prep_report = version.get('xsl_prep_report', None)
        self.xsl_preview = version.get('xsl_preview', None)
        self.dtd_filename = version.get('dtd_filename', None)
        self.css_filename = version.get('css_filename', None)
        self.xsl_output = version.get('xsl_output', None)
        self._report = []

    def log(self, content):
        print(content)

    def report(self, content):
        print(content)
        self._report.append(content)

    def _style_checker_report(self, xml_filename, html_report):
        # STYLE CHECKER REPORT
        report_ok = False
        xml_report = html_report.replace('.html', '.xml')
        if xml_transform(xml_filename, self.xsl_prep_report, xml_report):
            # Generate self.report.html
            #self.log('transform ' + xml_report + ' ' + self.xsl_report + ' ' + html_report)
            if xml_transform(xml_report, self.xsl_report, html_report):
                os.unlink(xml_report)

                f = open(html_report, 'r')
                c = f.read()
                f.close()

                report_ok = ('Total of errors = 0' in c)

                if report_ok:
                    self.report('Validation report. No errors found. Read ' + html_report)
                else:
                    self.report('Validation report. Some errors were found. Read ' + html_report)
            else:
                self.report('Unable to create validation report: ' + html_report)
        else:
            self.report('Unable to generate xml for report: ' + xml_report)
        return report_ok

    def _preview(self, xml_filename, html_preview, img_path, new_name=''):
        preview_ok = False
        if type(self.xsl_preview) == type([]):
            preview_ok = tranform_in_steps(xml_filename, self.xsl_preview, html_preview, {'path_img': img_path + '/', 'css':  self.css_filename, 'new_name': new_name})
        else:
            #self.log('transform ' + xml_filename + ' ' + self.xsl_preview + ' ' + html_preview)
            preview_ok = xml_transform(xml_filename, self.xsl_preview, html_preview, {'path_img': img_path + '/', 'css':  self.css_filename, 'new_name': new_name})

        if preview_ok:
            self.report('Preview ' + html_preview)
        else:
            self.report('Unable to create preview: ' + html_preview)
        return preview_ok

    def _output(self, xml_filename, xml_output):
        output_ok = False
        output_ok = xml_transform(xml_filename, self.xsl_output, xml_output)
        if output_ok:
            self.report('XML output ' + xml_output)
        else:
            self.report('Unable to create output: ' + xml_output)
        return output_ok

    def check_list(self, data):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)

        step_results = []

        self.report('\nValidating:' + data.xml_filename)

        if xml_is_well_formed(data.xml_filename):
            step_results.append(True)

            # VALIDATION
            is_dtd_valid = xml_validate(data.xml_filename, data.dtd_validation_report, (self.dtd_filename != ''))
            if not is_dtd_valid:
                self.report('Validation errors. Read ' + data.dtd_validation_report)
            step_results.append(is_dtd_valid)

            # STYLE CHECKER REPORT
            step_results.append(self._style_checker_report(data.xml_filename, data.html_report))

            # PREVIEW
            if data.html_preview:
                step_results.append(self._preview(data.xml_filename, data.html_preview))

            if data.output_filename:
                step_results.append(self._preview(data.xml_filename, data.output_filename))

        else:
            # not well formed
            self.report('Not well formed.')

        for f in data.result_filenames:
            if os.path.exists(f):
                print('Check ' + f)

        return all(step_results)


class XMLMetadata:
    def __init__(self, content):
        self.root = etree.parse(StringIO(content))

    def _meta_xml(self, node):
        issn, volid, issueno, suppl, fpage, order = ['', '', '', '', '', '']
        issn = self.root.findtext('.//front/journal-meta/issn[1]')
        volid = node.findtext('./volume')
        issueno = node.findtext('./issue')
        suppl = node.findtext('./supplement')
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
            if node:
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
                if int(fpage) == 0:
                    # use order
                else:
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

            if suppl:
                suppl = 's' + suppl if suppl != '0' else 'suppl'
            if issueno:
                issueno = '00' + issueno
                issueno = issueno[-2:]

            r = '-'.join([issn, param_acron, vol, issueno, suppl, page_or_order])

        return r

    def xml_data_image_names(self):
        test_href = ['href', 'xlink:href', '{http://www.w3.org/XML/1998/namespace}href']

        nodes = self.root.findall('.//*[graphic]')
        r = []
        for n in nodes:
            id = n.attrib.get('id')
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
                        r.append(href, id)
                        break
        return r

    def new_name_and_img_list(self, acron, alternative_id=''):        
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        xml_images_list = self.xml_data_image_names()
        return (new_name, xml_images_list)


class XMLPkgMker:

    def __init__(self, src_path, scielo_path, pmc_path, report_path, work_path, acron, version):
        self.src_path = src_path
        self.scielo_path = scielo_path
        self.pmc_path = pmc_path
        self.report_path = report_path
        self.acron = acron
        self.work_path = work_path
        self.version = version

        for d in [scielo_path, pmc_path, report_path, work_path]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    os.unlink(d + '/' + f)
            else:
                os.makedirs(d)

    def _normalize_xml(self, filename):
        """
        Normalize XML content
        """
        f = open(self.src_path + '/' + xml_file, 'r')
        content = f.read()
        f.close()

        content = normalize_entities(content)
        if xml_file.endswith('.sgm.xml'):
            content = SGMLXML().fix(content)
            new_name, img_list = XMLMetadata(content).new_name_and_img_list(acron, alternative_id)
            content = xml_content_transform(content, _versions_[self.version]['sgm2xml'])
        else:
            new_name, img_list = XMLMetadata(content).new_name_and_img_list(acron, alternative_id)
        return content, new_name, img_list

    def make_packages(self):
        img_to_jpeg(self.src_path, self.work_path)

        xml_files = [f for f in os.listdir(self.src_path) if f.endswith('.xml')]

        sci_validations = XMLValidations(_versions_[self.version]['scielo'])
        pmc_validations = XMLValidations(_versions_[self.version]['pmc'])

        for xml_file in xml_files:
            content, new_name, img_list = self._normalize_xml(self.src_path + '/' + xml_file)
            if xml_is_well_formed(content):
                xml_filename = self.work_path + '/' + xml_file.replace('.sgm.xml', '.xml')
                f = open(xml_filename, 'w')
                f.write(content)
                f.close()



            else:
                print('Unable to load ' + xml_file)


        self._xml2pmc()
