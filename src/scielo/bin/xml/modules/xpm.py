import os
import shutil
from datetime import datetime

from modules import article
from modules import xml_utils


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


def pack_related_files(src_path, dest_path, curr_and_new_href_list):
    not_found = []
    for curr, new in curr_and_new_href_list:
        f = src_path + '/' + curr
        if os.path.isfile(f):
            shutil.copyfile(f, dest_path + '/' + new)
        else:
            not_found.append(f)
    return not_found


def x(content, acron, xml_name):
    if xml_utils.is_xml_well_formed(content) is not None:
        doc = Article(content)
        new_name = format_new_name(doc, acron, xml_name)
        attach_info = get_attach_info(doc)
        print('href_list')
        print(attach_info)
        print(get_curr_and_new_href_list(xml_name, new_name, attach_info))
        if is_sgmxml:
            #href and new href list
            curr_and_new_href_list = get_curr_and_new_href_list(xml_name, new_name, attach_info)
            content = normalize_href(content, curr_and_new_href_list)
        else:
            new_name = xml_name
            curr_and_new_href_list = [(href, href) for href, item_id in new_href_list]
        print(curr_and_new_href_list)
        # related files and href files list
        not_found, related_files_list, href_files_list = self.matched_files(xml_name, new_name, curr_and_new_href_list, src_path)

        jpg_created = self.pack_related_files(related_files_list, href_files_list, src_path, dest_path)

        f = open(dest_path + '/' + new_name + '.xml', 'w')
        f.write(content)
        f.close()

        log.append('XML name:' + new_name)
        log.append('Total of related files: ' + str(len(related_files_list)))
        log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(related_files_list)]))

        log.append('Total of @href in XML: ' + str(len(href_list)))
        log.append('\n'.join(['   ' + c for c, n in sorted(href_list)]))

        if is_sgmxml:
            log.append('Renaming @href files in XML: ' + str(len(curr_and_new_href_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(curr_and_new_href_list)]))

            log.append('Renaming and packing @href files \n' + src_path + ' => packages: ' + str(len(href_files_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(href_files_list)]))
            log.append('\n'.join(jpg_created))
        else:
            log.append('Packing @href files \n' + src_path + ' => packages: ' + str(len(href_files_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(href_files_list)]))

        if len(not_found) > 0:
            log.append('\nTotal of @href files not found in ' + src_path + ': \n' + '\n'.join(sorted(not_found)))
    else:
        log.append('XML is not well formed')
        log.append(dest_path + '/incorrect_' + new_name + '.xml')

        f = open(dest_path + '/incorrect_' + new_name + '.xml', 'w')
        f.write(content)
        f.close()
    return (new_name, log)


def process_files(xml_filename, scielo_pkg_path, report_path, wrk_path):
    xml_path = os.path.dirname(xml_filename)
    xml_file = os.path.basename(xml_filename)

    xml_name = xml_file.replace('.sgm.xml', '').replace('.xml', '')
    xml_wrk_path = wrk_path + '/' + xml_name

    log_filename = report_path + '/' + xml_name + '.log'
    err_filename = report_path + '/' + xml_name + '.err.txt'

    clean_folder(xml_wrk_path)
    delete_files([log_filename, err_filename])


def process(xml_files, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path):
    for xml_filename in xml_files:
        process_file(xml_filename, scielo_pkg_path, report_path, wrk_path)
    hdimages_to_jpeg(scielo_pkg_path, scielo_pkg_path, True)
    
