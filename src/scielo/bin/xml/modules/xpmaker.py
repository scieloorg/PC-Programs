# coding=utf-8
import os
import shutil
from datetime import datetime

from modules import article
from modules import files_manager
from modules import java_xml_utils
from modules import xml_utils
from modules import xml_versions
from modules import pkg_checker
from modules import xpchecker
from modules import reports


html_report = reports.ReportHTML()
messages = []
log_items = []


def register_message(message):
    if not '<' in message:
        message = html_report.format_message(message)
    messages.append(message)


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


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
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    xml, e = xml_utils.load_xml(content)
    if xml is None:
        content = fix_sgml_xml(content)
        xml, e = xml_utils.load_xml(content)
    if e is None:
        content = java_xml_utils.xml_content_transform(content, xml_versions.xsl_sgml2xml(version))
    else:
        print(e)
    if isinstance(content, unicode):
        content = content.encode('utf-8')
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
    files_manager.delete_files([dest_path + '/' + f for f in os.listdir(dest_path) if f.endswith('.sgm.xml')])
    return (related_files_list, href_files_list, not_found)


def pack_file_extended(src_path, dest_path, curr, new):
    r = []
    c = curr if not '.' in curr else curr[0:curr.rfind('.')]
    n = new if not '.' in new else new[0:new.rfind('.')]
    found = [f for f in os.listdir(src_path) if (f.startswith(c + '.') or f.startswith('-')) and not f.startswith('.sgm.xml')]
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

    register_log(doc_files_info.xml_name)
    register_log('start')
    report_content = ''
    content = open(doc_files_info.xml_filename, 'r').read()
    #register_log(content)
    register_log('remove_doctype')
    content = xml_utils.remove_doctype(content)
    #register_log(content)

    register_log('convert_entities_to_chars')
    content, replaced_named_ent = xml_utils.convert_entities_to_chars(content)
    #register_log(content)

    if doc_files_info.is_sgmxml:
        register_log('normalize_sgmlxml')
        content = normalize_sgmlxml(doc_files_info.xml_name, content, doc_files_info.xml_path, version, doc_files_info.html_filename)
        #register_log(content)

    new_name = doc_files_info.xml_name
    register_log('load_xml')
    xml, e = xml_utils.load_xml(content)
    
    if not xml is None:
        doc = article.Article(xml)
        register_log('get_attach_info')
        attach_info = get_attach_info(doc)
        if doc_files_info.is_sgmxml:
            register_log('format_new_name')
            new_name = format_new_name(doc, acron, doc_files_info.xml_name)
            register_log('get_curr_and_new_href_list')
            curr_and_new_href_list = get_curr_and_new_href_list(doc_files_info.xml_name, new_name, attach_info)
            register_log('add_extension')
            curr_and_new_href_list = add_extension(curr_and_new_href_list, doc_files_info.xml_path)
            register_log('normalize_hrefs')
            content = normalize_hrefs(content, curr_and_new_href_list)
        else:
            curr_and_new_href_list = [(href, href) for href, ign1, ign2 in attach_info]
            register_log('add_extension')
            curr_and_new_href_list = add_extension(curr_and_new_href_list, doc_files_info.xml_path)
        register_log('pack_files')
        related_packed, href_packed, not_found = pack_files(doc_files_info.xml_path, scielo_pkg_path, doc_files_info.xml_name, new_name, curr_and_new_href_list)
        register_log('pack_files_report')
        param_related_packed = ['   ' + c + ' => ' + n for c, n in related_packed]
        param_href_packed = ['   ' + c + ' => ' + n for c, n in href_packed]
        param_curr_and_new_href_list = ['   ' + c + ' => ' + n for c, n in curr_and_new_href_list]
        param_not_found = ['   ' + c + ' => ' + n for c, n in not_found]

        if len(replaced_named_ent) > 0:
            entities_report = 'Converted entities:' + '\n'.join(replaced_named_ent) + '-'*30
        else:
            entities_report = ''
        report_content = entities_report + packed_files_report(doc_files_info.xml_name, new_name, doc_files_info.xml_path, scielo_pkg_path, param_related_packed, param_href_packed, param_curr_and_new_href_list, param_not_found)
        open(doc_files_info.err_filename, 'w').write(report_content)

    new_xml_filename = scielo_pkg_path + '/' + new_name + '.xml'

    register_log('new_xml_filename')
    content = xml_utils.replace_doctype(content, xml_versions.DTDFiles('scielo', version).doctype)
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    open(new_xml_filename, 'w').write(content)
    print(' ... created')
    register_log('end')
    return (new_name, new_xml_filename)


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


def get_href_list(xml_filename):
    href_list = []
    xml, e = xml_utils.load_xml(xml_filename)
    if not xml is None:
        doc = article.Article(xml)
        attach_info = get_attach_info(doc)
        href_list = [href for href, attach_type, attach_id in attach_info]
    return href_list


def xml_output(xml_filename, xsl_filename, result_filename):
    if os.path.exists(result_filename):
        os.unlink(result_filename)
    return java_xml_utils.xml_transform(xml_filename, xsl_filename, result_filename)


def generate_and_validate_package(xml_files, markup_xml_path, acron, version='1.0'):
    from_markup = any([f.endswith('.sgm.xml') for f in xml_files])

    do_toc_report = not from_markup
    do_pmc_package = from_markup

    scielo_pkg_path = markup_xml_path + '/scielo_package'
    pmc_pkg_path = markup_xml_path + '/pmc_package'
    report_path = markup_xml_path + '/errors'
    wrk_path = markup_xml_path + '/work'

    report_names = {}
    xml_to_validate = []

    pmc_dtd_files = xml_versions.DTDFiles('pmc', version)
    scielo_dtd_files = xml_versions.DTDFiles('scielo', version)

    for d in [scielo_pkg_path, pmc_pkg_path, report_path, wrk_path]:
        if not os.path.isdir(d):
            os.makedirs(d)

    if len(xml_files) > 0:
        path = xml_files[0]
        path = os.path.dirname(path)
        hdimages_to_jpeg(path, path, False)

    print('Generate packages for ' + str(len(xml_files)) + ' files.')
    for xml_filename in xml_files:

        doc_files_info = files_manager.DocumentFiles(xml_filename, report_path, wrk_path)
        doc_files_info.clean()
        if doc_files_info.is_sgmxml:
            do_toc_report = False

        new_name, new_xml_filename = generate_article_xml_package(doc_files_info, scielo_pkg_path, version, acron)
        doc_files_info.new_name = new_name
        doc_files_info.new_xml_filename = new_xml_filename
        doc_files_info.new_xml_path = os.path.dirname(new_xml_filename)

        report_names[new_name] = doc_files_info.xml_name
        xml_to_validate.append(doc_files_info)

        if not doc_files_info.is_sgmxml:
            if do_pmc_package:
                loaded_xml, e = xml_utils.load_xml(new_xml_filename)
                if loaded_xml is not None:
                    doc = article.Article(loaded_xml)
                    do_pmc_package = (doc.journal_id_nlm_ta is not None)

        if do_pmc_package:
            register_log('xml_output')
            pmc_xml_filename = pmc_pkg_path + '/' + new_name + '.xml'
            xml_output(doc_files_info.new_xml_filename, scielo_dtd_files.xsl_output, pmc_xml_filename)

            print(' ... created pmc')
            register_log(' ... created pmc')
            #validation of pmc.xml
            register_log('validate_article_xml pmc')
            loaded_xml, is_valid_dtd, is_valid_style = xpchecker.validate_article_xml(pmc_xml_filename, pmc_dtd_files, doc_files_info.pmc_dtd_report_filename, doc_files_info.pmc_style_report_filename, doc_files_info.ctrl_filename, None)
            if loaded_xml is not None:
                xml_output(pmc_xml_filename, pmc_dtd_files.xsl_output, pmc_xml_filename)

    print('Generate validation reports...')
    validate_created_package(scielo_pkg_path, xml_to_validate, scielo_dtd_files, report_path, do_toc_report, not from_markup)

    # termina de montar o pacote inteiro do pmc
    if do_pmc_package:
        for f in os.listdir(scielo_pkg_path):
            if not f.endswith('.xml') and not f.endswith('.jpg'):
                shutil.copyfile(scielo_pkg_path + '/' + f, pmc_pkg_path + '/' + f)

    print('Result of the processing:')
    print(markup_xml_path)

    s = '\n'.join(log_items)
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    open(report_path + '/log.txt', 'w').write(s)


def validate_created_package(scielo_pkg_path, doc_files_info_list, dtd_files, report_path, do_toc_report, display_report):

    register_log('generate validations reports')

    issues, toc_results, articles, articles_stats, article_results = pkg_checker.validate_package(doc_files_info_list, dtd_files, report_path, False, do_toc_report)

    register_message(articles_stats)

    if do_toc_report:
        toc_stats_numbers, toc_stats_report = toc_results
        toc_f, toc_e, toc_w = toc_stats_numbers

        register_message(toc_stats_report)
        if toc_f + toc_e + toc_w > 0:
            register_message(html_report.link('file:///' + report_path + '/toc.html', 'toc.html'))
        register_message(html_report.link('file:///' + report_path + '/authors.html', 'authors.html'))
        register_message(html_report.link('file:///' + report_path + '/sources.html', 'sources.html'))

    register_message('\n'.join([item[2] for item in article_results.values()]))
    register_message('Result of the processing: ' + html_report.link('file:///' + os.path.dirname(scielo_pkg_path), os.path.dirname(scielo_pkg_path)))
    html_report.title = ['Validations report', scielo_pkg_path]
    html_report.body = '\n'.join(messages)
    html_report.save(report_path + '/xml_package_maker.html')
    print('\n\nXML Package Maker reports:\n ' + report_path + '/xml_package_maker.html')
    if display_report:
        pkg_checker.display_report(report_path + '/xml_package_maker.html')


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
        generate_and_validate_package(xml_files, markup_xml_path, acron, version)
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
