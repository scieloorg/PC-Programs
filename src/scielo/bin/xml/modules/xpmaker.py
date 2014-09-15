import os
import shutil
import tempfile
from datetime import datetime

from modules import article
from modules import xml_utils
from modules import java_xml_utils
from modules import xpchecker
from modules import reports


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))


DEFAULT_VERSION = '1.0'
PMC_PATH = THIS_LOCATION + '/../../pmc'

XSL_SGML2XML = {}
XSL_SGML2XML['3.0'] = PMC_PATH + '/v3.0/xsl/sgml2xml/sgml2xml.xsl'
XSL_SGML2XML['1.0'] = PMC_PATH + '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

DOCTYPE = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">'

XPM_FILES = {}
XPM_FILES['scielo3.0'] = {}
XPM_FILES['scielo3.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
XPM_FILES['scielo3.0']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
XPM_FILES['scielo3.0']['css'] = PMC_PATH + '/v3.0/xsl/web/plus'
XPM_FILES['scielo3.0']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/scielo-style/stylechecker.xsl'
XPM_FILES['scielo3.0']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
XPM_FILES['scielo3.0']['xsl_preview'] = PMC_PATH + '/v3.0/xsl/previewers/scielo-html-novo.xsl'
XPM_FILES['scielo3.0']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/xml2pmc.xsl'

XPM_FILES['pmc3.0'] = {}
XPM_FILES['pmc3.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
XPM_FILES['pmc3.0']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
XPM_FILES['pmc3.0']['css'] = PMC_PATH + '/v3.0/xsl/jpub/jpub-preview.css'
XPM_FILES['pmc3.0']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
XPM_FILES['pmc3.0']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
XPM_FILES['pmc3.0']['xsl_preview'] = [PMC_PATH + '/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
XPM_FILES['pmc3.0']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/pmc.xsl'

XPM_FILES['scielo1.0'] = {}
XPM_FILES['scielo1.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
XPM_FILES['scielo1.0']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.0']['css'] = XPM_FILES['scielo3.0']['css']
XPM_FILES['scielo1.0']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/scielo-style/stylechecker.xsl'
XPM_FILES['scielo1.0']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.4/style-reporter.xsl'
XPM_FILES['scielo1.0']['xsl_preview'] = XPM_FILES['scielo3.0']['xsl_preview']
XPM_FILES['scielo1.0']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/xml2pmc.xsl'

XPM_FILES['pmc1.0'] = {}
XPM_FILES['pmc1.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
XPM_FILES['pmc1.0']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.0']['css'] = XPM_FILES['pmc3.0']['css']
XPM_FILES['pmc1.0']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.4/nlm-stylechecker.xsl'
XPM_FILES['pmc1.0']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.4/style-reporter.xsl'
XPM_FILES['pmc1.0']['xsl_preview'] = [PMC_PATH + '/j1.0/xsl/jpub/citations-prep/jpub1-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
XPM_FILES['pmc1.0']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/pmc.xsl'


def xsl_sgml2xml(version):
    return XSL_SGML2XML.get(version, DEFAULT_VERSION)


class DTDFiles(object):

    def __init__(self, database_name, version):
        self.database_name = database_name
        self.version = version
        self.data = XPM_FILES.get(database_name + DEFAULT_VERSION, {})

    @property
    def doctype(self):
        return self.data['doctype']

    @property
    def dtd_filename(self):
        return self.data['dtd']

    @property
    def xsl_prep_report(self):
        return self.data['xsl_prep_report']

    @property
    def xsl_report(self):
        return self.data['xsl_report']

    @property
    def xsl_output(self):
        return self.data['xsl_output']


class XMLContent(object):

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
        self.content = self.content.replace(' '*2, ' '*1)
        if xml_utils.is_xml_well_formed(self.content) is None:
            self._fix_style_tags()
        if xml_utils.is_xml_well_formed(self.content) is None:
            self._fix_open_close()

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
            rcontent = rcontent.replace('<' + tag.upper() + '>', '<' + tag + '>')
            rcontent = rcontent.replace('</' + tag.upper() + '>', '</' + tag + '>')
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')
        if self.content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            self.content = self._fix_problem(tag_list, parts)
        for tag in tags:
            self.content = self.content.replace('</' + tag + '><' + tag + '>', '')

    def _fix_problem(self, tag_list, parts):
        expected_close_tags = []
        ign_list = []
        debug = False
        k = 0
        for part in parts:
            if part in tag_list:
                tag = part
                if debug:
                    print('\ncurrent:' + tag)
                if tag.startswith('</'):
                    if debug:
                        print('expected')
                        print(expected_close_tags)
                        print('ign_list')
                        print(ign_list)
                    if tag in ign_list:
                        if debug:
                            print('remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:
                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)
                            if not matched:
                                if debug:
                                    print('not matched')
                                while not matched and len(expected_close_tags) > 0:
                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]
                                    matched = (expected_close_tags[-1] == tag)
                                if debug:
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


class DocFilesInfo(object):

    def __init__(self, xml_filename, report_path, wrk_path):
        self.xml_filename = xml_filename
        self.xml_path = os.path.dirname(xml_filename)

        xml_file = os.path.basename(xml_filename)
        self.xml_name = xml_file.replace('.sgm.xml', '').replace('.xml', '')

        self.xml_wrk_path = wrk_path + '/' + self.xml_name

        self.dtd_validation_report_filename = report_path + '/' + self.xml_name + '.dtd.txt'
        self.style_checker_report_filename = report_path + '/' + self.xml_name + '.rep.html'

        self.pmc_dtd_validation_report_filename = report_path + '/' + self.xml_name + '.pmc.dtd.txt'
        self.pmc_style_checker_report_filename = report_path + '/' + self.xml_name + '.pmc.rep.html'

        self.err_filename = report_path + '/' + self.xml_name + '.err.txt'
        self.html_filename = self.xml_wrk_path + '/' + self.xml_name + '.temp.htm'
        if not os.path.isfile(self.html_filename):
            self.html_filename += 'l'

        self.is_sgmxml = xml_filename.endswith('.sgm.xml')
        self.ctrl_filename = self.err_filename.replace('.err', '.ctrl') if self.is_sgmxml else None

    def clean(self):
        clean_folder(self.xml_wrk_path)
        delete_files([self.err_filename, self.dtd_validation_report_filename, self.style_checker_report_filename, self.pmc_dtd_validation_report_filename, self.pmc_style_checker_report_filename, self.ctrl_filename])


def rename_embedded_img_href(content, xml_name, new_href_list):
    content = content.replace('<graphic href="?', '--FIXHREF--<graphic href="?')
    items = content.split('--FIXHREF--')
    new = ''
    i = 0
    for item in items:
        if item.startswith('<graphic href="?'):
            s = item[item.find('?'):]
            new += '<graphic href="' + xml_name + new_href_list[i] + s[s.find('"'):]
            i += 1
        else:
            new += item
    return new


def html_img_src(html_content):
    #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
    #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
    html_content = html_content.replace('[graphic href="?', '[graphic href="?' + '"--FIXHREF--FIXHREF')
    items = [item for item in html_content.split('--FIXHREF--') if item.startswith('FIXHREF')]
    img_src = []
    for item in items:
        if ' src="' in item:
            item = item[item.find(' src="') + len(' src="')]
            item = item[0:item.find('"')]
            item = item[item.find('/') + 1:]
            if len(item) > 0:
                img_src.append(item)
    return img_src


def extract_embedded_images(xml_name, content, html_filename, dest_path):
    if content.find('href="?' + xml_name):
        html_content = open(html_filename, 'r').read()
        embedded_img_files = html_img_src(html_content)
        embedded_img_path = os.path.dirname(html_filename)
        content = rename_embedded_img_href(content, xml_name, embedded_img_files)
        for item in embedded_img_files:
            if os.path.isfile(embedded_img_path + '/' + item):
                shutil.copyfile(embedded_img_path + '/' + item, dest_path + '/' + xml_name + item)
    return content


def normalize_sgmlxml(xml_name, content, src_path, version, html_filename):
    content = extract_embedded_images(xml_name, content, html_filename, src_path)
    if not xml_utils.is_xml_well_formed(content):
        content = fix_sgml_xml(content)
    if xml_utils.is_xml_well_formed(content) is not None:
        content = java_xml_utils.xml_content_transform(content, xsl_sgml2xml(version))
    return content


def fix_sgml_xml(content):
    xml_fix = XMLContent(content)
    xml_fix.fix()
    if not xml_fix.content == content:
        content = xml_fix.content
    return content


def hdimages_to_jpeg(source_path, jpg_path, replace=False):
    try:
        import Image
        IMG_CONVERTER = True
    except:
        IMG_CONVERTER = False

    if IMG_CONVERTER:
        for item in os.listdir(source_path):
            image_filename = source_path + '/' + item
            jpg_filename = source_path + '/' + item[0:item.rfind('.')] + '.jpg'
            if item.endswith('.tiff') or item.endswith('.eps') or item.endswith('.tif'):
                doit = False
                if os.path.isfile(jpg_filename):
                    if replace:
                        doit = True
                else:
                    doit = True
                if doit:
                    try:
                        im = Image.open(image_filename)
                        im.thumbnail(im.size)
                        im.save(jpg_filename, "JPEG")
                    except Exception as inst:
                        print('Unable to generate ' + jpg_filename)
                        print(inst)


def clean_folder(path):
    if os.path.isdir(path):
        for f in os.listdir(path):
            if os.path.isfile(path + '/' + f):
                os.unlink(path + '/' + f)
    else:
        os.makedirs(path)


def delete_files(files):
    for f in files:
        if f is not None:
            if os.path.isfile(f):
                os.unlink(f)


def format_new_name(doc, param_acron='', original_xml_name=''):
    def format_last_part(fpage, seq, elocation_id, order, doi, issn):
        def normalize_len(fpage):
            fpage = '00000' + fpage
            return fpage[-5:]
        print((fpage, seq, elocation_id, order, doi, issn))
        r = None
        if r is None:
            if fpage is not None:
                r = normalize_len(fpage)
                if seq is not None:
                    r += '-' + seq
        if r is None:
            if elocation_id is not None:
                r = elocation_id
        if r is None:
            if doi is not None:
                doi = doi[doi.find('/')+1:]
                if issn in doi:
                    doi = doi[doi.find(issn) + len(issn):]
                doi = doi.replace('.', '_').replace('-', '_')
                r = doi
        if r is None:
            if order is not None:
                r = normalize_len(order)
        return r
    r = ''
    vol, issueno, fpage, seq, elocation_id, order, doi = doc.volume, doc.number, doc.fpage, doc.fpage_seq, doc.elocation_id, doc.order, doc.doi
    issn = doc.e_issn if doc.e_issn else doc.print_issn
    suppl = doc.volume_suppl if doc.volume_suppl else doc.number_suppl
    if original_xml_name != '':
        issn = original_xml_name[0:9]
    last = format_last_part(fpage, seq, elocation_id, order, doi, issn)
    if issueno:
        if issueno == 'ahead' or issueno == '00':
            issueno = None
        else:
            if len(issueno) <= 2:
                issueno = '00' + issueno
                issueno = issueno[-2:]
    if suppl:
        suppl = 's' + suppl if suppl != '0' else 'suppl'
    parts = [issn, param_acron, vol, issueno, suppl, last]
    r = '-'.join([part for part in parts if part is not None and not part == ''])
    return r


def href_attach_type(parent_tag, tag):
    if 'suppl' in tag or 'media' == tag:
        attach_type = 's'
    elif 'inline' in tag:
        attach_type = 'i'
    elif parent_tag in ['equation', 'disp-formula']:
        attach_type = 'e'
    else:
        attach_type = 'g'
    return attach_type


def get_curr_and_new_href_list(xml_name, new_name, href_list):
    r = []
    attach_type = ''
    for href, attach_type, attach_id in href_list:
        if attach_id is None:
            attach_name = href.replace(xml_name, '')
        else:
            attach_name = attach_id
            if '.' in href:
                attach_name += href[href.rfind('.'):]
        new = new_name + '-' + attach_type + attach_name
        r.append((href, new))
    return list(set(r))


def get_attach_info(doc):
    items = []
    for href_info in doc.hrefs:
        if href_info.isfile:
            attach_type = href_attach_type(href_info.parent.tag, href_info.element.tag)
            attach_id = href_info.id
            items.append((href_info.src, attach_type, attach_id))
    return items


def normalize_hrefs(content, curr_and_new_href_list):
    for current, new in curr_and_new_href_list:
        print(current + ' => ' + new)
        content = content.replace('href="' + current, 'href="' + new)
    return content


def pack_files(src_path, dest_path, xml_name, new_name, href_files_list):
    related_files_list = []
    href_files_list = []
    not_found = []
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    for f in get_related_files(src_path, xml_name):
        related_files_list += pack_file_extended(src_path, dest_path, f, f.replace(xml_name, new_name))
    for curr, new in href_files_list:
        s = pack_file_extended(src_path, dest_path, curr, new)
        if len(s) == 0:
            not_found.append((curr, new))
        else:
            href_files_list += s
    return (related_files_list, href_files_list, not_found)


def pack_file_extended(src_path, dest_path, curr, new):
    r = []
    c = curr if not '.' in curr else curr[0:curr.rfind('.')]
    n = new if not '.' in new else new[0:new.rfind('.')]
    found = [f for f in os.listdir(src_path) if f.startswith(c + '.') or f.startswith('-')]
    for f in found:
        shutil.copyfile(src_path + '/' + f, dest_path + '/' + f.replace(c, n))
        r.append((f, f.replace(c, n)))
    return r


def packed_files_report(xml_name, new_name, src_path, dest_path, related_files_list, href_files_list, href_list, not_found):

    log = []

    log.append('Report of files\n' + '-'*len('Report of files') + '\n')

    if src_path != dest_path:
        log.append('Source path:   ' + src_path)
    log.append('Package path:  ' + dest_path)
    if src_path != dest_path:
        log.append('Source XML name: ' + xml_name)
    log.append('Package XML name: ' + new_name)

    log.append(message_file_list('Total of related files', related_files_list))
    log.append(message_file_list('Total of @href in XML', href_list))
    log.append(message_file_list('Total of @href files', href_files_list))
    log.append(message_file_list('Total of @href files which were not found', not_found))

    return '\n'.join(log)


def message_file_list(label, file_list):
    return '\n' + label + ': ' + str(len(file_list)) + '\n' + '\n'.join(sorted(file_list))


def generate_article_xml_package(doc_files_info, scielo_pkg_path, version, acron):
    print('.....')
    print(doc_files_info.xml_name)
    print('-'*len(doc_files_info.xml_name))

    report_content = ''

    content = open(doc_files_info.xml_filename, 'r').read()
    if '\n<!DOCTYPE' in content:
        temp = content[content.find('\n<!DOCTYPE'):]
        temp = temp[0:temp.find('>')+1]
        content = content.replace(temp, '')

    content = xml_utils.convert_entities_to_chars(content)
    if doc_files_info.is_sgmxml:
        content = normalize_sgmlxml(doc_files_info.xml_name, content, doc_files_info.xml_path, version, doc_files_info.html_filename)

    new_name = doc_files_info.xml_name
    xml = xml_utils.load_xml(content)
    if not xml is None:
        doc = article.Article(xml)
        attach_info = get_attach_info(doc)
        if doc_files_info.is_sgmxml:
            new_name = format_new_name(doc, acron, doc_files_info.xml_name)
            curr_and_new_href_list = get_curr_and_new_href_list(doc_files_info.xml_name, new_name, attach_info)
            content = normalize_hrefs(content, curr_and_new_href_list)
        else:
            curr_and_new_href_list = [(href, href) for href, ign1, ign2 in attach_info]

        related_packed, href_packed, not_found = pack_files(doc_files_info.xml_path, scielo_pkg_path, doc_files_info.xml_name, new_name, curr_and_new_href_list)

        param_related_packed = ['   ' + c + ' => ' + n for c, n in related_packed]
        param_href_packed = ['   ' + c + ' => ' + n for c, n in href_packed]
        param_curr_and_new_href_list = ['   ' + c + ' => ' + n for c, n in curr_and_new_href_list]
        param_not_found = ['   ' + c + ' => ' + n for c, n in not_found]

        report_content = packed_files_report(doc_files_info.xml_name, new_name, doc_files_info.xml_path, scielo_pkg_path, param_related_packed, param_href_packed, param_curr_and_new_href_list, param_not_found)

    new_xml_filename = scielo_pkg_path + '/' + new_name + '.xml'
    open(new_xml_filename, 'w').write(content)
    print(' ... created')

    return (new_name, new_xml_filename, report_content)


def get_related_files(path, name):
    return [f for f in os.listdir(path) if f.startswith(name + '.') or f.startswith(name + '-')]


def get_not_found(path, href_list):
    not_found = []
    for href in href_list:
        if not os.path.isfile(path + '/' + href_list):
            not_found.append(href)
    return not_found


def get_not_found_extended(path, href_list):
    not_found = []
    for href in href_list:
        if not os.path.isfile(path + '/' + href_list):
            if '.' in href:
                t = href[0:href.rfind('.')]
            else:
                t = href
            found = [f for f in os.listdir(path) if f.startswith(t)]
            if len(found) == 0:
                not_found.append(href)
    return not_found


def get_href_list(xml_filename):
    href_list = []
    xml = xml_utils.load_xml(xml_filename)
    if not xml is None:
        doc = article.Article(xml)
        attach_info = get_attach_info(doc)
        href_list = [href for href, attach_type, attach_id in attach_info]
    return href_list


def apply_dtd(content, dtd_filename, doctype):
    xml_str = XMLContent(content)
    xml_str.fix_dtd_location(dtd_filename, doctype)
    return xml_str.content


def evaluate_article_xml(xml_filename, dtd_files, dtd_validation_report_filename, style_checker_report_filename):

    def get_temp_filename(xml_filename):
        temp_dir = tempfile.mkdtemp()
        return temp_dir + '/' + os.path.basename(xml_filename)

    xml = None
    is_valid_dtd = False
    is_valid_style = False

    if os.path.isfile(xml_filename):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)

        content = open(xml_filename, 'r').read()

        xml = xml_utils.load_xml(content)

        content = apply_dtd(content, dtd_files.dtd_filename, dtd_files.doctype)
        temp_filename = get_temp_filename(xml_filename)
        open(temp_filename, 'w').write(content)

        is_valid_dtd = xpchecker.dtd_validation(temp_filename, dtd_validation_report_filename)

        if xml is not None:
            is_valid_style = xpchecker.style_validation(temp_filename, style_checker_report_filename, dtd_files.xsl_prep_report, dtd_files.xsl_report)
        else:
            is_valid_style = False

        os.unlink(temp_filename)
        shutil.rmtree(os.path.dirname(temp_filename))
        
    return (xml, is_valid_dtd, is_valid_style)


def manage_result_files(ctrl_filename, is_valid_dtd, is_valid_style, dtd_validation_report, style_checker_report):
    if ctrl_filename is None:
        if is_valid_style is True:
            os.unlink(style_checker_report)
    else:
        open(ctrl_filename, 'w').write('Finished')
    if os.path.isfile(dtd_validation_report):
        os.unlink(dtd_validation_report)


def xml_output(xml_filename, xsl_filename, result_filename):
    if os.path.exists(result_filename):
        os.unlink(result_filename)
    return java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)


def process_articles(xml_files, markup_xml_path, acron, version='1.0'):
    do_toc_report = False

    scielo_pkg_path = markup_xml_path + '/scielo_package'
    pmc_pkg_path = markup_xml_path + '/pmc_package'
    report_path = markup_xml_path + '/errors'
    wrk_path = markup_xml_path + '/work'

    for d in [scielo_pkg_path, pmc_pkg_path, report_path]:
        if not os.path.isdir(d):
            os.makedirs(d)

    xml_names = {}
    if len(xml_files) > 0:
        path = xml_files[0]
        path = os.path.dirname(path)
        hdimages_to_jpeg(path, path, False)

    print('Generate packages (' + str(len(xml_files)) + '):')
    for xml_filename in xml_files:
        doc_files_info = DocFilesInfo(xml_filename, report_path, wrk_path)
        doc_files_info.clean()

        do_toc_report = not doc_files_info.is_sgmxml

        new_name, new_xml_filename, report_content = generate_article_xml_package(doc_files_info, scielo_pkg_path, version, acron)
        doc_files_info.new_name = new_name
        doc_files_info.new_xml_filename = new_xml_filename

        xml_names[new_name] = doc_files_info.xml_name

        # validation of scielo.xml
        dtd_files = DTDFiles('scielo', version)
        loaded_xml, is_valid_dtd, is_valid_style = evaluate_article_xml(doc_files_info.new_xml_filename, dtd_files, doc_files_info.dtd_validation_report_filename, doc_files_info.style_checker_report_filename)
        print(' ... validated')
        if os.path.isfile(doc_files_info.dtd_validation_report_filename):
            report_content += '\n\n\n' + '.........\n\n\n' + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(doc_files_info.dtd_validation_report_filename, 'r').read()
        open(doc_files_info.err_filename, 'w').write(report_content)

        # manage result
        manage_result_files(doc_files_info.ctrl_filename, is_valid_dtd, is_valid_style, doc_files_info.dtd_validation_report_filename, doc_files_info.style_checker_report_filename)

        if loaded_xml is not None:
            #generation of pmc.xml
            xml_output(doc_files_info.new_xml_filename, dtd_files.xsl_output, pmc_pkg_path + '/' + doc_files_info.new_name + '.xml')

            #validation of pmc.xml
            dtd_files = DTDFiles('pmc', version)
            loaded_xml, is_valid_dtd, is_valid_style = evaluate_article_xml(pmc_pkg_path + '/' + doc_files_info.new_name + '.xml', dtd_files, doc_files_info.pmc_dtd_validation_report_filename, doc_files_info.pmc_style_checker_report_filename)

            # manage result
            manage_result_files(doc_files_info.ctrl_filename, is_valid_dtd, is_valid_style, doc_files_info.pmc_dtd_validation_report_filename, doc_files_info.pmc_style_checker_report_filename)

    print('Generate contents validation reports...')
    reports.generate_package_reports(scielo_pkg_path, xml_names, report_path, do_toc_report)

    print('Reports')
    print(report_path)
    # termina de montar o pacote inteiro do pmc
    for f in os.listdir(scielo_pkg_path):
        if not f.endswith('.xml') and not f.endswith('.jpg'):
            shutil.copyfile(scielo_pkg_path + '/' + f, pmc_pkg_path + '/' + f)


def validate_path(path):
    xml_files = []
    markup_xml_path = ''
    if path is not None:
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[0:-1]
        if len(path) > 0:
            if os.path.isdir(path):
                xml_files = [path + '/' + f for f in os.listdir(path) if f.endswith('.xml')]
                now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
                now = now[0:now.find('.')]
                markup_xml_path = os.path.dirname(path) + '/' + now
                if not os.path.isdir(markup_xml_path):
                    os.makedirs(markup_xml_path)
            elif os.path.isfile(path):
                if path.endswith('.sgm.xml'):
                    # path = ?/markup_xml/work/<name>/<name>.sgm.xml
                    # f = <name>.sgm.xml
                    f = os.path.basename(path)
                    #src_path = ?/markup_xml/work/<name>
                    markup_xml_path = os.path.dirname(path)
                    #markup_xml_path = ?/markup_xml/work
                    markup_xml_path = os.path.dirname(markup_xml_path)
                    #markup_xml_path = ?/markup_xml
                    markup_xml_path = os.path.dirname(markup_xml_path)
                    #markup_xml_path = ?/src
                    src_path = markup_xml_path + '/src'
                    if not os.path.isdir(src_path):
                        os.makedirs(src_path)
                    shutil.copyfile(path, src_path + '/' + f)
                    xml_files = [src_path + '/' + f]
                elif path.endswith('.xml'):
                    xml_files = [path]
                    now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
                    now = now[0:now.find('.')]
                    markup_xml_path = os.path.dirname(os.path.dirname(path)) + '/' + now
                    if not os.path.isdir(markup_xml_path):
                        os.makedirs(markup_xml_path)
    return (xml_files, markup_xml_path)


def make_packages(path, acron, version):
    xml_files, markup_xml_path = validate_path(path)
    if len(xml_files) == 0:
        print('There is nothing to process.\n')
        print(path)
        print(' must be an XML file or a folder which contains XML files.')
    else:
        process_articles(xml_files, markup_xml_path, acron, version)
        print('Result of the processing:')
        print(markup_xml_path)
        print(' -- the end -- ')


def read_inputs(args):
    path = None
    acron = ''

    if len(args) == 3:
        script, path, acron = args
        if not os.path.isfile(path) and not os.path.isdir(path):
            path = None

    if path is None:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python xml_package_maker <xml_src> <acron>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filename or path which contains XML files')
        messages.append('  <acron> = journal acronym')
        acron = '\n'.join(messages)
        print(args)
    return (path, acron)


def call_make_packages(args, version):
    path, acron = read_inputs(args)
    if path is None:
        print(acron)
    else:
        make_packages(path, acron, version)
