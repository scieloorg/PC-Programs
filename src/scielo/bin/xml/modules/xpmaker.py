# coding=utf-8
import os
import shutil
import urllib
from datetime import datetime
from mimetypes import MimeTypes

import article
import serial_files
import java_xml_utils
import xml_utils
import xml_versions
import pkg_reports
import xpchecker
import fs_utils


mime = MimeTypes()
messages = []
log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def replace_mimetypes(content, path):
    r = content
    if 'mimetype="replace' in content:
        content = content.replace('mimetype="replace', '_~BREAK~MIME_MIME:')
        content = content.replace('mime-subtype="replace"', '_~BREAK~MIME_')
        r = ''
        for item in content.split('_~BREAK~MIME_'):
            if item.startswith('MIME:'):
                f = item[5:]
                f = f[0:f.rfind('"')]
                result = ''
                if os.path.isfile(path + '/' + f):
                    result = mime.guess_type(path + '/' + f)
                else:
                    url = urllib.pathname2url(f)
                    result = mime.guess_type(url)
                try:
                    result = result[0]
                    if '/' in result:
                        m, ms = result.split('/')
                        r += 'mimetype="' + m + '" mime-subtype="' + ms + '"'
                    else:
                        pass
                except:
                    pass
            else:
                r += item
    else:
        print('.............')
    return r


def rename_embedded_img_href(content, xml_name, new_href_list):
    content = content.replace('<graphic href="?', '--FIXHREF--<graphic href="?')
    _items = content.split('--FIXHREF--')
    new = content
    print(new_href_list)
    if len(new_href_list) == (len(_items) - 1):
        new = ''
        i = 0
        for item in _items:
            if item.startswith('<graphic href="?'):
                s = item[item.find('?'):]
                s = s[s.find('"'):]
                new += '<graphic href="' + xml_name + new_href_list[i] + s
                i += 1
            else:
                new += item
    else:
        print('rename_embedded_img_href')
        print(new_href_list)
        print(len(new_href_list))
        print(len(_items))
    return new


def get_embedded_images_in_html(html_content):
    #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
    #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
    if 'href=&quot;?' in html_content:
        html_content = html_content.replace('href=&quot;?', 'href="?')
    if '“' in html_content:
        html_content = html_content.replace('“', '"')
    if '”' in html_content:
        html_content = html_content.replace('”', '"')

    html_content = html_content.replace('href="?', 'href="?--~BREAK~FIXHREF--FIXHREF')
    _items = html_content.split('--~BREAK~FIXHREF--')
    items = [item for item in _items if item.startswith('FIXHREF')]

    img_src = []
    for item in items:
        if 'src="' in item:
            src = item[item.find('src="') + len('src="'):]
            src = src[0:src.find('"')]
            if '/' in src:
                src = src[src.find('/') + 1:]
            if len(src) > 0:
                img_src.append(src)
    return img_src


def extract_embedded_images(xml_name, content, html_content, html_filename, dest_path):
    if content.find('href="?' + xml_name):
        embedded_img_files = get_embedded_images_in_html(html_content)
        embedded_img_path = None

        html_path = os.path.dirname(html_filename)
        html_name = os.path.basename(html_filename)
        html_name = html_name[0:html_name.rfind('.')]

        for item in os.listdir(html_path):
            if os.path.isdir(html_path + '/' + item) and item.startswith(html_name):
                embedded_img_path = html_path + '/' + item
                break
        if not embedded_img_path is None:
            content = rename_embedded_img_href(content, xml_name, embedded_img_files)
            for item in embedded_img_files:
                if os.path.isfile(embedded_img_path + '/' + item):
                    shutil.copyfile(embedded_img_path + '/' + item, dest_path + '/' + xml_name + item)
                    print(dest_path + '/' + xml_name + item)
        content = content.replace('"">', '">')
        content = content.replace('href=""?', 'href="?')

    return content


def get_html_tables(html_content):
    html_content = fix_sgml_tags(html_content)
    #print(html_content)
    html_content = fix_tabwrap_end(html_content)
    #print(html_content)

    tables = {}
    html_content = html_content.replace('[tabwrap', '~BREAK~[tabwrap')
    html_content = html_content.replace('[/tabwrap]', '[/tabwrap]~BREAK~')
    for item in html_content.split('~BREAK~'):
        if item.startswith('[tabwrap') and item.endswith('[/tabwrap]'):
            table_id = item[item.find('id="')+len('id="'):]
            table_id = table_id[0:table_id.find('"')]
            table = item[item.find('<table'):]
            table = table[0:table.rfind('</table>')+len('</table>')]

            table = remove_sgml_tags(table)
            table = ignore_html_tags_and_insert_quotes_to_attributes(table, ['table', 'a', 'img', 'tbody', 'thead', 'th', 'tr', 'td', 'b', 'i'])
            print(table_id)
            print(table)
            x
            tables[table_id] = table
    return tables


def fix_sgml_tags(html_content):
    # [<span style='color:#666699'>/td]
    html_content = html_content.replace('[', '~BREAK~[')
    html_content = html_content.replace(']', ']~BREAK~')
    new = []
    for item in html_content.split('~BREAK~'):
        if item.startswith('[') and item.endswith(']') and '<' in item and '>' in item:
            p1 = item.find('<')
            p2 = item.find('>')
            if p1 < p2:
                r = item[p1:p2+1]
                if r.startswith('</'):
                    item = r + item[0:p1] + item[p2+1:]
                else:
                    item = item[0:p1] + item[p2+1:] + r

        new.append(item)
    return ''.join(new)


def remove_sgml_tags(html_content):
    html_content = html_content.replace('[', '~BREAK~[')
    html_content = html_content.replace(']', ']~BREAK~')
    parts = []
    for part in html_content.split('~BREAK~'):
        if not part.startswith('[') and not part.endswith(']'):
            parts.append(part)
    return ''.join(parts)


def ignore_html_tags_and_insert_quotes_to_attributes(html_content, tags_to_keep, html=True):
    if html:
        c1 = '<'
        c2 = '>'
    else:
        c1 = '['
        c2 = ']'
    html_content = html_content.replace(c1, '~BREAK~' + c1)
    html_content = html_content.replace(c2, c2 + '~BREAK~')

    html_content = html_content.replace(' nowrap', '')
    parts = []
    for part in html_content.split('~BREAK~'):
        if part.startswith(c1) and part.endswith(c2):
            tag = part[1:]
            if tag.startswith('/'):
                tag = tag[1:-1]
            else:
                if ' ' in tag:
                    tag = tag[0:tag.find(' ')]
                else:
                    tag = tag[0:tag.find(c2)]

            if tag in tags_to_keep:
                if '=' in part:
                    print('-'*80)
                    print(part)
                    open_tag = part.replace(c2, ' ' + c2)
                    open_tag = open_tag.replace('=', '~BREAK~=')
                    attributes = []
                    for attr in open_tag.split('~BREAK~'):
                        if attr.startswith('='):
                            if not '"' in attr:
                                attr = attr.replace('=', '="')
                                p = attr.rfind(' ')
                                attr = attr[0:p] + '"' + attr[p:]
                        attributes.append(attr)
                    part = ''.join(attributes).replace(' ' + c2, c2)
                    print(part)
            else:
                part = ''
        parts.append(part)
    return ''.join(parts)


def fix_tabwrap_end(html_content):
    html_content = html_content.replace('[tabwrap', '~BREAK~[tabwrap')
    parts = []
    for part in html_content.split('~BREAK~'):
        if part.startswith('[tabwrap'):
            p_table = part.find('</table>')
            p_tabwrap = part.find('[/tabwrap]')
            if p_tabwrap < p_table:
                part = part.replace('[/tabwrap]', '')
                part = part.replace('</table>', '</table>[/tabwrap]')
        parts.append(part)
    return ''.join(parts)


def replace_tables_in_sgmlxml(content, embedded_tables):
    for table_id, table in embedded_tables.items():
        p = content.find('<tabwrap id="' + table_id + '"')
        if p > 0:
            t = content[p:]
            p_end = t.find('</table>')
            if p_end > 0:
                p_end += len('</table>')
                t = t[0:p_end]
                p = t.find('<table')
                if p > 0:
                    t = t[p:]
                    content = content.replace(t, table)

    return content


def read_html(html_filename):
    html_content = open(html_filename, 'r').read()
    if not '<html' in html_content.lower():
        c = html_content
        for c in html_content:
            if ord(c) == 0:
                break
        html_content = html_content.replace(c, '')
    return html_content


def normalize_sgmlxml(xml_name, content, src_path, version, html_filename):
    #content = fix_uppercase_tag(content)
    register_log('normalize_sgmlxml')

    html_content = read_html(html_filename)

    #embedded_tables = get_html_tables(html_content)
    #content = replace_tables_in_sgmlxml(content, embedded_tables)
    content = extract_embedded_images(xml_name, content, html_content, html_filename, src_path)

    xml = xml_utils.is_xml_well_formed(content)
    if xml is None:
        content = fix_sgml_xml(content)
        xml = xml_utils.is_xml_well_formed(content)
    if not xml is None:
        content = java_xml_utils.xml_content_transform(content, xml_versions.xsl_sgml2xml(version))
        content = replace_mimetypes(content, src_path)
    else:
        pass
    return content


def fix_sgml_xml(content):
    xml_fix = xml_utils.XMLContent(content)
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


def generate_new_name(doc, param_acron='', original_xml_name=''):
    def format_last_part(fpage, seq, elocation_id, order, doi, issn):
        def normalize_len(fpage):
            fpage = '00000' + fpage
            return fpage[-5:]
        #print((fpage, seq, elocation_id, order, doi, issn))
        r = None
        if r is None:
            if fpage is not None:
                r = normalize_len(fpage)
                if seq is not None:
                    r += '-' + seq
                if r == '00000':
                    r = None
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

    register_log('generate_new_name')

    r = ''
    vol, issueno, fpage, seq, elocation_id, order, doi = doc.volume, doc.number, doc.fpage, doc.fpage_seq, doc.elocation_id, doc.order, doc.doi

    issns = [issn for issn in [doc.e_issn, doc.print_issn] if issn is not None]
    if original_xml_name[0:9] in issns:
        issn = original_xml_name[0:9]
    else:
        issn = doc.e_issn if doc.e_issn else doc.print_issn

    suppl = doc.volume_suppl if doc.volume_suppl else doc.number_suppl

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
    parts = [issn, param_acron, vol, issueno, suppl, last, doc.compl]
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


def generate_curr_and_new_href_list(xml_name, new_name, href_list):
    r = []
    attach_type = ''
    for href, attach_type, attach_id in href_list:
        if attach_id is None:
            attach_name = href.replace(xml_name, '')
            if attach_name[0:1] in '-_':
                attach_name = attach_name[1:]
        else:
            attach_name = attach_id
            if '.' in href:
                attach_name += href[href.rfind('.'):]
        new = new_name + '-' + attach_type + attach_name
        r.append((href, new))
    return list(set(r))


def add_extension(curr_and_new_href_list, xml_path):
    r = []
    for href, new_href in curr_and_new_href_list:
        if not '.' in new_href:
            extensions = [f[f.rfind('.'):] for f in os.listdir(xml_path) if f.startswith(href + '.')]
            if len(extensions) > 1:
                extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
            if len(extensions) > 0:
                new_href += extensions[0]
        r.append((href, new_href))
    return r


def get_attach_info(doc):
    items = []
    for href_info in doc.hrefs:
        if href_info.is_internal_file:
            attach_type = href_attach_type(href_info.parent.tag, href_info.element.tag)
            attach_id = href_info.id
            items.append((href_info.src, attach_type, attach_id))
    return items


def normalize_hrefs(content, curr_and_new_href_list):
    for current, new in curr_and_new_href_list:
        print(current + ' => ' + new)
        content = content.replace('href="' + current, 'href="' + new)
    return content


def pack_article_files(doc_files_info, dest_path, href_files_list):
    src_path = doc_files_info.xml_path
    xml_name = doc_files_info.xml_name
    new_name = doc_files_info.new_name

    r_related_files_list = []
    r_href_files_list = []
    r_not_found = []

    related_files_list = get_related_files(src_path, xml_name)

    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    for f in related_files_list:
        r_related_files_list += pack_file_extended(src_path, dest_path, f, f.replace(xml_name, new_name))
    for curr, new in href_files_list:
        s = pack_file_extended(src_path, dest_path, curr, new)
        if len(s) == 0:
            r_not_found.append((curr, new))
        else:
            r_href_files_list += s
    serial_files.delete_files([dest_path + '/' + f for f in os.listdir(dest_path) if f.endswith('.sgm.xml')])

    return (r_related_files_list, r_href_files_list, r_not_found)


def pack_file_extended(src_path, dest_path, curr, new):
    r = []
    c = curr if not '.' in curr else curr[0:curr.rfind('.')]
    n = new if not '.' in new else new[0:new.rfind('.')]
    found = [f for f in os.listdir(src_path) if (f == curr or f.startswith(c + '.') or f.startswith(c + '-')) and not f.endswith('.sgm.xml') and not f.endswith('.replaced.txt') and not f.endswith('.xml.bkp')]
    for f in found:
        shutil.copyfile(src_path + '/' + f, dest_path + '/' + f.replace(c, n))
        r.append((f, f.replace(c, n)))
    return r


def generate_packed_files_report(doc_files_info, dest_path, related_packed, href_packed, curr_and_new_href_list, not_found):

    def format(files_list):
        return ['   ' + c + ' => ' + n for c, n in files_list]

    xml_name = doc_files_info.xml_name
    new_name = doc_files_info.new_name
    src_path = doc_files_info.xml_path

    log = []

    log.append('Report of files\n' + '-'*len('Report of files') + '\n')

    if src_path != dest_path:
        log.append('Source path:   ' + src_path)
    log.append('Package path:  ' + dest_path)
    if src_path != dest_path:
        log.append('Source XML name: ' + xml_name)
    log.append('Package XML name: ' + new_name)

    log.append(message_file_list('Total of related files', format(related_packed)))
    log.append(message_file_list('Total of @href in XML', format(href_packed)))
    log.append(message_file_list('Total of files in package', format(curr_and_new_href_list)))
    log.append(message_file_list('Total of files not found in package', format(not_found)))

    return '\n'.join(log)


def message_file_list(label, file_list):
    return '\n' + label + ': ' + str(len(file_list)) + '\n' + '\n'.join(sorted(file_list))


def normalize_xml_content(doc_files_info, content, version):
    register_log('normalize_xml_content')

    register_log('remove_doctype')
    content = xml_utils.remove_doctype(content)

    register_log('convert_entities_to_chars')
    content, replaced_named_ent = xml_utils.convert_entities_to_chars(content)

    content = xml_utils.pretty_print(content)

    replaced_entities_report = ''
    if len(replaced_named_ent) > 0:
        replaced_entities_report = 'Converted entities:' + '\n'.join(replaced_named_ent) + '-'*30

    if doc_files_info.is_sgmxml:
        content = normalize_sgmlxml(doc_files_info.xml_name, content, doc_files_info.xml_path, version, doc_files_info.html_filename)

    return (content, replaced_entities_report)


def get_new_name(doc_files_info, doc, acron):
    new_name = doc_files_info.xml_name
    if doc_files_info.is_sgmxml:
        new_name = generate_new_name(doc, acron, doc_files_info.xml_name)
    return new_name


def get_curr_and_new_href_list(doc_files_info, doc):
    attach_info = get_attach_info(doc)

    if doc_files_info.is_sgmxml:
        register_log('generate_curr_and_new_href_list')
        curr_and_new_href_list = generate_curr_and_new_href_list(doc_files_info.xml_name, doc_files_info.new_name, attach_info)
    else:
        curr_and_new_href_list = [(href, href) for href, ign1, ign2 in attach_info]
    register_log('add_extension')
    return add_extension(curr_and_new_href_list, doc_files_info.xml_path)


def pack_xml_file(content, version, new_xml_filename, do_incorrect_copy=False):
    register_log('pack_xml_file')
    content = xml_utils.replace_doctype(content, xml_versions.DTDFiles('scielo', version).doctype)
    fs_utils.write_file(new_xml_filename, content)

    if do_incorrect_copy is None:
        shutil.copyfile(new_xml_filename, new_xml_filename.replace('.xml', '_incorrect.xml'))


def normalize_package_name(doc_files_info, acron, content):
    register_log('load_xml')
    xml, e = xml_utils.load_xml(content)

    doc = article.Article(xml) if xml is not None else None
    doc_files_info.new_name = doc_files_info.xml_name
    curr_and_new_href_list = None

    if not doc is None:
        register_log('get_attach_info')

        doc_files_info.new_name = get_new_name(doc_files_info, doc, acron)
        curr_and_new_href_list = get_curr_and_new_href_list(doc_files_info, doc)

        if doc_files_info.is_sgmxml:
            register_log('normalize_hrefs')
            content = normalize_hrefs(content, curr_and_new_href_list)

            xml, e = xml_utils.load_xml(content)
            doc = article.Article(xml) if xml is not None else None

    doc_files_info.new_xml_filename = doc_files_info.new_xml_path + '/' + doc_files_info.new_name + '.xml'
    return (doc, doc_files_info, curr_and_new_href_list, content)


def make_article_package(doc_files_info, scielo_pkg_path, version, acron):
    packed_files_report = ''
    content = open(doc_files_info.xml_filename, 'r').read()

    print('.....')
    print(doc_files_info.xml_name)
    print('-'*len(doc_files_info.xml_name))

    register_log(doc_files_info.xml_name)

    register_log('normalize_xml_content')
    content, replaced_entities_report = normalize_xml_content(doc_files_info, content, version)

    register_log('normalize_package_name')
    doc_files_info.new_xml_path = scielo_pkg_path
    doc, doc_files_info, curr_and_new_href_list, content = normalize_package_name(doc_files_info, acron, content)

    if not doc is None:
        register_log('pack_article_files')
        related_packed, href_packed, not_found = pack_article_files(doc_files_info, scielo_pkg_path, curr_and_new_href_list)

        register_log('pack_article_files_report')
        packed_files_report = generate_packed_files_report(doc_files_info, scielo_pkg_path, related_packed, href_packed, curr_and_new_href_list, not_found)

    pack_xml_file(content, version, doc_files_info.new_xml_filename, (doc is None))

    if isinstance(replaced_entities_report, unicode):
        replaced_entities_report = replaced_entities_report.encode('utf-8')

    open(doc_files_info.err_filename, 'w').write(replaced_entities_report + packed_files_report)

    print(' ... created')

    return (doc, doc_files_info)


def get_related_files(path, name):
    return [f for f in os.listdir(path) if (f.startswith(name + '.') or f.startswith(name + '-')) and not f.startswith('.sgm.xml')]


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


def xml_output(xml_filename, doctype, xsl_filename, result_filename):
    if result_filename == xml_filename:
        shutil.copyfile(xml_filename, xml_filename + '.bkp')
        xml_filename = xml_filename + '.bkp'
    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp = xml_utils.apply_dtd(xml_filename, doctype)
    r = java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)
    xml_utils.restore_xml_file(xml_filename, temp)
    if xml_filename.endswith('.bkp'):
        os.unlink(xml_filename)
    return r


def zip_package(pkg_path, zip_name):
    import zipfile
    zipf = zipfile.ZipFile(zip_name, 'w')
    for root, dirs, files in os.walk(pkg_path):
        for file in files:
            zipf.write(os.path.join(root, file), arcname=os.path.basename(file))
    zipf.close()


def make_package(xml_files, report_path, wrk_path, scielo_pkg_path, version, acron):
    print('Make packages for ' + str(len(xml_files)) + ' files.')
    r = []
    for xml_filename in xml_files:

        doc_files_info = serial_files.DocumentFiles(xml_filename, report_path, wrk_path)
        doc_files_info.clean()

        doc, doc_files_info = make_article_package(doc_files_info, scielo_pkg_path, version, acron)

        #report_names[doc_files_info.new_name] = doc_files_info.xml_name
        r.append((doc, doc_files_info))
    return r


def make_pmc_package(articles, scielo_pkg_path, pmc_pkg_path, scielo_dtd_files, pmc_dtd_files):
    done = False
    for doc, doc_files_info in articles:
        if doc.journal_id_nlm_ta is not None:
            print('.....')
            print(doc_files_info.xml_name)
            print('-'*len(doc_files_info.xml_name))

            pmc_xml_filename = pmc_pkg_path + '/' + doc_files_info.new_name + '.xml'
            xml_output(doc_files_info.new_xml_filename, scielo_dtd_files.doctype_with_local_path, scielo_dtd_files.xsl_output, pmc_xml_filename)

            print(' ... created pmc')
            register_log(' ... created pmc')
            #validation of pmc.xml
            register_log('validate_article_xml pmc')
            xpchecker.style_validation(pmc_xml_filename, pmc_dtd_files.doctype_with_local_path, doc_files_info.pmc_style_report_filename, pmc_dtd_files.xsl_prep_report, pmc_dtd_files.xsl_report, pmc_dtd_files.database_name)
            xml_output(pmc_xml_filename, pmc_dtd_files.doctype_with_local_path, pmc_dtd_files.xsl_output, pmc_xml_filename)
            done = True
    if done:
        for f in os.listdir(scielo_pkg_path):
            if not f.endswith('.xml') and not f.endswith('.jpg'):
                shutil.copyfile(scielo_pkg_path + '/' + f, pmc_pkg_path + '/' + f)
        zip_packages(pmc_pkg_path)


def pack_and_validate(xml_files, source_parent_path, acron, version, from_converter=False):
    from_markup = any([f.endswith('.sgm.xml') for f in xml_files])

    do_toc_report = not from_markup

    scielo_pkg_path = source_parent_path + '/scielo_package'
    pmc_pkg_path = source_parent_path + '/pmc_package'
    report_path = source_parent_path + '/errors'
    wrk_path = source_parent_path + '/work'

    pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    for d in [scielo_pkg_path, pmc_pkg_path, report_path, wrk_path]:
        if not os.path.isdir(d):
            os.makedirs(d)

    if len(xml_files) == 0:
        print('No files to process')
    else:
        path = xml_files[0]
        path = os.path.dirname(path)
        hdimages_to_jpeg(path, path, False)

        pkg_items = make_package(xml_files, report_path, wrk_path, scielo_pkg_path, version, acron)

        generate_reports(pkg_items, scielo_dtd_files, scielo_pkg_path, report_path, do_toc_report, not from_markup, from_converter)

        if not from_converter:
            zip_packages(scielo_pkg_path)
            make_pmc_package(pkg_items, scielo_pkg_path, pmc_pkg_path, scielo_dtd_files, pmc_dtd_files)

        print('Result of the processing:')
        print(source_parent_path)

        s = '\n'.join(log_items)

        fs_utils.write_file(report_path + '/log.txt', s)


def zip_packages(src_pkg_path):
    names = [item[0:item.rfind('-')] for item in os.listdir(src_pkg_path) if item.endswith('.xml') and '-' in item]
    names = list(set(names))
    path = src_pkg_path + '_zips'
    for name in names:
        new_pkg_path = path + '/' + name
        if not os.path.isdir(new_pkg_path):
            os.makedirs(new_pkg_path)
        for item in os.listdir(new_pkg_path):
            os.unlink(new_pkg_path + '/' + item)
        for item in os.listdir(src_pkg_path):
            if item.startswith(name):
                shutil.copyfile(src_pkg_path + '/' + item, new_pkg_path + '/' + item)
        zip_package(new_pkg_path, new_pkg_path + '.zip')
        for item in os.listdir(new_pkg_path):
            os.unlink(new_pkg_path + '/' + item)
        shutil.rmtree(new_pkg_path)


def generate_reports(pkg_items, dtd_files, scielo_pkg_path, report_path, do_toc_report, display_report, from_converter):

    validate_order = from_converter

    content = pkg_reports.xml_list(scielo_pkg_path)
    content += pkg_reports.package_validations_report(pkg_items, dtd_files, validate_order, do_toc_report)
    content += pkg_reports.processing_result_location(scielo_pkg_path)

    filename = report_path + '/xml_package_maker.html'
    pkg_reports.save_report(filename, 'XML Package Maker Report', content)

    if display_report:
        pkg_reports.display_report(filename)


def validate_path(path):
    xml_files = []
    markup_xml_path = ''
    if path is not None:
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[0:-1]
        if len(path) > 0:
            if os.path.isdir(path):
                xml_files = sorted([path + '/' + f for f in os.listdir(path) if f.endswith('.xml')])
                #now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
                #now = now[0:now.find('.')]
                now = 'xml_package_maker_result'
                markup_xml_path = path + '_' + now
                fs_utils.delete_file_or_folder(markup_xml_path)
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


def get_articles(xml_path):
    r = {}
    for xml_filename in os.listdir(xml_path):
        if xml_filename.endswith('.xml'):
            xml, e = xml_utils.load_xml(xml_path + '/' + xml_filename)
            doc = article.Article(xml) if xml is not None else None
            r[xml_filename] = doc
    return r


def get_pkg_items(xml_filenames, report_path):
    r = []
    for xml_filename in xml_filenames:
        doc_files_info = serial_files.DocumentFiles(xml_filename, report_path, None)
        doc_files_info.new_xml_filename = xml_filename
        doc_files_info.new_xml_path = os.path.dirname(xml_filename)

        xml, e = xml_utils.load_xml(doc_files_info.new_xml_filename)
        doc = article.Article(xml) if xml is not None else None
        r.append((doc, doc_files_info))
    return r


def package_issue(package_info):
    issue_label = []
    e_issn = []
    print_issn = []
    for doc, doc_files_info in package_info:
        if doc is not None:
            issue_label.append(doc.issue_label)
            if doc.e_issn is not None:
                e_issn.append(doc.e_issn)
            if doc.print_issn is not None:
                print_issn.append(doc.print_issn)
    issue_label = list(set(issue_label))
    e_issn = list(set(e_issn))
    print_issn = list(set(print_issn))

    issue_label = issue_label[0] if len(issue_label) == 1 else None
    e_issn = e_issn[0] if len(e_issn) > 0 else None
    print_issn = print_issn[0] if len(print_issn) > 0 else None
    return (issue_label, e_issn, print_issn)


def make_packages(path, acron, version):
    xml_files, markup_xml_path = validate_path(path)
    if len(xml_files) == 0:
        print('There is nothing to process.\n')
        print(path)
        print(' must be an XML file or a folder which contains XML files.')
    else:
        pack_and_validate(xml_files, markup_xml_path, acron, version)
        print('finished')


def read_inputs(args):
    script = args[0]
    path = None
    acron = ''
    if len(args) == 3:
        script, path, acron = args
        path = path.replace('\\', '/')
        if not os.path.isfile(path) and not os.path.isdir(path):
            path = None

    if path is None:
        messages = []
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python ' + script + ' <xml_src> <acron>')
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


def is_valid_xml_path(xml_path):
    total = 0
    if os.path.isdir(xml_path):
        total = len([item for item in os.listdir(xml_path) if item.endswith('.xml')])
    return total > 0


def validate_inputs(xml_path, acron):
    errors = []
    if xml_path is None:
        errors.append('Missing XML location.')
    else:
        if os.path.isfile(xml_path):
            if not xml_path.endswith('.xml'):
                errors.append('Invalid file. XML file required.')
        elif not is_valid_xml_path(xml_path):
            errors.append('Invalid folder. Folder must have XML files.')
    if acron is None:
        errors.append('Missing acronym.')
    return errors
