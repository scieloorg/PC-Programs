import os
import shutil
from datetime import datetime

from modules import article
from modules import xml_utils
from modules import sgml2xml


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
        if os.path.isfile(f):
            os.unlink(f)


def xml_paths(src):
    now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
    now = now[0:now.find('.')]

    if os.path.isfile(src):
        path = os.path.dirname(src) + '_' + now
    else:
        path = src + '_' + now

    scielo_pkg_path = path + '/scielo_package'
    pmc_pkg_path = path + '/pmc_package'
    report_path = path + '/errors'
    wrk_path = path + '/wrk'
    preview_path = None
    return (scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def markup_paths(source_path, sgmxml_filename):
    sgmxml_path = os.path.dirname(sgmxml_filename)
    markup_xml_path = os.path.dirname(source_path)

    scielo_pkg_path = markup_xml_path + '/scielo_package'
    pmc_pkg_path = markup_xml_path + '/pmc_package'
    report_path = markup_xml_path + '/errors'
    preview_path = None
    wrk_path = sgmxml_path
    return (scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def markup_src_path(sgmxml_filename):
    # sgmxml_path = serial/acron/issue/pmc/pmc_work/article
    # sgmxml_path = serial/acron/issue/markup_xml/work/article
    xml_name = os.path.basename(sgmxml_filename)
    sgmxml_path = os.path.dirname(sgmxml_filename)

    # markup_xml_path = serial/acron/issue/pmc
    # markup_xml_path = serial/acron/issue/markup_xml
    markup_xml_path = os.path.dirname(os.path.dirname(sgmxml_path))

    # other files path = serial/acron/issue/pmc/src or serial/acron/issue/pmc/pmc_src
    # other files path = serial/acron/issue/markup_xml/src
    source_path = markup_xml_path + '/src'
    if not os.path.isdir(source_path):
        source_path = markup_xml_path + '/pmc_src'
    if not os.path.isdir(source_path):
        os.makedirs(source_path)
    shutil.copyfile(sgmxml_filename, source_path + '/' + xml_name)
    return source_path


def files_and_paths(xml_source):
    if xml_source.endswith('.sgm.xml'):
        f = xml_source
        ctrl_filename = f.replace('.sgm.xml', '.ctrl.txt')
        source_path = markup_src_path(f)
        xml_files = [source_path + '/' + os.path.basename(f)]
        scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = markup_paths(source_path, f)
        #version = 'j1.0'
    else:
        if os.path.isfile(xml_source):
            xml_files = [xml_source]
        else:
            xml_files = [xml_source + '/' + f for f in os.listdir(xml_source) if f.endswith('.xml')]
        ctrl_filename = None
        scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = xml_paths(xml_source)

    return (ctrl_filename, xml_files, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


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
            attach_name = attach_id + href[href.rfind('.'):]
        new = new_name + '-' + attach_type + attach_name
        r.append((href, new))
    return list(set(r))


def get_attach_info(doc):
    items = []
    for href_info in doc.hrefs:
        attach_type = href_attach_type(href_info.parent.tag, href_info.element_name)
        attach_id = href_info.id
        items.append((href_info.src, attach_type, attach_id))
    return items


def replace_hrefs(content, curr_and_new_href_list):
    #print(curr_and_new_href_list)
    for current, new in curr_and_new_href_list:
        print(current + ' => ' + new)
        content = content.replace('href="' + current, 'href="' + new)
    return content


def normalize_hrefs(content, acron, xml_name):
    curr_and_new_href_list = []
    if xml_utils.is_xml_well_formed(content) is not None:
        doc = article.Article(content)
        new_name = format_new_name(doc, acron, xml_name)
        attach_info = get_attach_info(doc)
        print('href_list')
        print(attach_info)
        curr_and_new_href_list = get_curr_and_new_href_list(xml_name, new_name, attach_info)
        print(curr_and_new_href_list)
        content = replace_hrefs(content, curr_and_new_href_list)
    return (new_name, curr_and_new_href_list, content)


def pack_related_files(src_path, xml_name, new_name, dest_path, curr_and_new_href_list):
    not_found = []
    related_files_list = []
    href_files_list = []
    href_list = []
    for f in os.listdir(src_path):
        if f.startswith(xml_name + '.') and not f.endswith(xml_name + '.sgm.xml'):
            new = f.replace(xml_name, new_name)
            related_files_list.append((f, new))
            shutil.copyfile(src_path + '/' + f, dest_path + '/' + new)
    for curr, new in curr_and_new_href_list:
        href_list.append((curr, new))
        f = src_path + '/' + curr
        if os.path.isfile(f):
            if curr.rfind('.') > 0:
                curr_name = curr[0:curr.rfind('.')]
                new_name = new[0:new.rfind('.')]
            else:
                curr_name = curr
                new_name = new
            for f in [f for f in os.listdir(src_path) if f.startswith(curr_name + '.')]:
                ext = f[f.rfind('.'):] if f.rfind('.') > 0 else ''
                href_files_list.append((f, new_name + ext))
                shutil.copy(src_path + '/' + f, dest_path + '/' + new_name + ext)
        else:
            not_found.append(curr)
    return (not_found, related_files_list, href_files_list, href_list)


def files_report(xml_name, new_name, src_path, dest_path, related_files_list, href_files_list, href_list, not_found):
    def display_sorted(pair):
        r = sorted(['   ' + c + ' => ' + n for c, n in pair])
        return '\n'.join(r)

    log = []

    log.append('Source path:   ' + src_path)
    log.append('Package path:  ' + dest_path)
    log.append('Source XML name:   ' + xml_name)
    log.append('Generated XML name:' + new_name)

    log.append('\nTotal of related files: ' + str(len(related_files_list)))
    log.append(display_sorted(related_files_list))

    log.append('\nTotal of @href in XML: ' + str(len(href_list)))
    log.append(display_sorted(href_list))

    log.append('\nPacking @href files: ' + str(len(href_files_list)))
    log.append(display_sorted(href_files_list))

    if len(not_found) > 0:
        log.append('\nERROR: Total of @href files not found in ' + src_path + ':')
        log.append(display_sorted(not_found))
    return '\n'.join(log)


def generate_article_xml_package(xml_filename, scielo_pkg_path, report_path, wrk_path, version, acron):
    xml_path = os.path.dirname(xml_filename)
    xml_file = os.path.basename(xml_filename)

    xml_name = xml_file.replace('.sgm.xml', '').replace('.xml', '')
    xml_wrk_path = wrk_path + '/' + xml_name

    err_filename = report_path + '/' + xml_name + '.err.txt'

    clean_folder(xml_wrk_path)
    delete_files([log_filename, err_filename])

    is_sgmxml = xml_filename.endswith('.sgm.xml')
    html_filename = ''

    content = open(xml_filename, 'r').read()

    content = xml_utils.convert_entities_to_chars(content)
    if is_sgmxml:
        html_filename = xml_wrk_path + '/' + xml_name + '.temp.htm'
        if not os.path.isfile(html_filename):
            html_filename += 'l'
        content = sgml2xml.normalize_sgmlxml(xml_name, content, xml_path, version, html_filename)

    if xml_utils.is_xml_well_formed(content) is None:
        new_xml_filename = scielo_pkg_path + '/incorrect_' + xml_name + '.xml'
        report_content = xml_file + ' is not well formed\nOpen ' + new_xml_filename + ' using an XML Editor.'
        r = False
    else:
        new_name = xml_name
        doc = article.Article(content)
        attach_info = get_attach_info(doc)

        print('attach_info')
        print(attach_info)

        if is_sgmxml:
            new_name = format_new_name(doc, acron, xml_name)
            curr_and_new_href_list = get_curr_and_new_href_list(xml_name, new_name, attach_info)
            content = sgml2xml.normalize_href(content, curr_and_new_href_list)
        else:
            curr_and_new_href_list = [(href, href) for href, attach_type, attach_id in attach_info]
        print(curr_and_new_href_list)

        # pack files
        not_found, related_files_list, href_files_list, href_list = pack_related_files(xml_path, xml_name, new_name, scielo_pkg_path, curr_and_new_href_list)
        r = True
        new_xml_filename = scielo_pkg_path + '/' + new_name + '.xml'
        report_content = files_report(xml_name, new_name, xml_path, scielo_pkg_path, related_files_list, href_files_list, href_list, not_found)
    try:
        open(new_xml_filename, 'w').write(content)
    except:
        print('ERROR: Unable to create ' + new_xml_filename)
    try:
        open(err_filename, 'w').write(report_content)
    except:
        print('ERROR: Unable to create ' + err_filename)

    return (r, new_xml_filename, err_filename)


def generate_issue_xml_package(xml_files, scielo_pkg_path, report_path, wrk_path, acron, version='1.0'):
    reports = {}
    hdimages_to_jpeg(scielo_pkg_path, scielo_pkg_path, False)
    for xml_filename in xml_files:
        r, new_xml_filename, err_filename = generate_article_xml_package(xml_filename, scielo_pkg_path, report_path, wrk_path, version, acron)
        reports[xml_filename] = (r, new_xml_filename, err_filename)
    return reports


def evaluate_article_xml_package():
