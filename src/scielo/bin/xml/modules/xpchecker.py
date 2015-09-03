# coding=utf-8
import os
from datetime import datetime

from __init__ import _
import fs_utils


IS_PACKTOOLS_INSTALLED = False
try:
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
except:
    os.environ['XML_CATALOG_FILES'] = ''


import java_xml_utils
import xml_utils
import html_reports


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def save_packtools_style_report(content, report_filename):
    version = ''
    try:
        import pkg_resources
        version = pkg_resources.get_distribution('packtools').version
    except:
        pass

    q = len(content.split('SPS-ERROR')) - 1
    msg = ''
    title = 'Style Checker (packtools' + version + ')'
    if q > 0:
        msg = html_reports.tag('div', 'Total of errors = ' + str(q), 'error')

    body = msg + ''.join([html_reports.display_xml(item, html_reports.XML_WIDTH*0.9) for item in content.split('\n')])
    html_reports.save(report_filename, title, body)


def packtools_dtd_validation(xml_filename, report_filename):
    import packtools
    xml_validator = packtools.stylechecker.XMLValidator(xml_filename)
    is_valid, errors = xml_validator.validate()
    r = '\n'.join([err.message for err in errors])
    fs_utils.write_file(report_filename, r)
    return is_valid


def packtools_style_validation(xml_filename, report_filename):
    from lxml import etree
    import packtools
    xml_validator = packtools.stylechecker.XMLValidator(xml_filename)
    is_valid, errors = xml_validator.validate()
    err_xml = xml_validator.annotate_errors()
    r = etree.tostring(err_xml, pretty_print=True, encoding='utf-8', xml_declaration=True)
    save_packtools_style_report(r, report_filename)
    f, e, w = style_checker_statistics(report_filename)
    return (f + e + w == 0)


def java_xml_utils_dtd_validation(xml_filename, report_filename, doctype):
    register_log('java_xml_utils_dtd_validation: inicio')
    r = java_xml_utils.xml_validate(xml_filename, report_filename, doctype)
    register_log('java_xml_utils_dtd_validation: fim')
    return r


def java_xml_utils_style_validation(xml_filename, doctype, report_filename, xsl_prep_report, xsl_report):
    # STYLE CHECKER REPORT
    register_log('java_xml_utils_style_validation: inicio')
    is_valid_style = False
    xml_report = report_filename.replace('.html', '.xml')
    if os.path.exists(xml_report):
        os.unlink(xml_report)
    if os.path.exists(report_filename):
        os.unlink(report_filename)

    parameters = {}
    bkp_xml_filename = xml_utils.apply_dtd(xml_filename, doctype)
    if java_xml_utils.xml_transform(xml_filename, xsl_prep_report, xml_report, parameters):
        #parameters = {'filename': xml_report}
        java_xml_utils.xml_transform(xml_report, xsl_report, report_filename, parameters)
    else:
        fs_utils.write_file(report_filename, 'FATAL ERROR: ' + _('Unable to create') + ' ' + report_filename)
    if os.path.isfile(report_filename):
        c = fs_utils.read_file(report_filename)
        is_valid_style = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))

    if os.path.isfile(bkp_xml_filename):
        xml_utils.restore_xml_file(xml_filename, bkp_xml_filename)

    if os.path.isfile(xml_report):
        os.unlink(xml_report)
    register_log('java_xml_utils_style_validation: fim')
    return is_valid_style


def style_checker_statistics(report_filename):
    total_f = 0
    total_e = 0
    total_w = 0
    if os.path.isfile(report_filename):
        content = open(report_filename, 'r').read()
        if 'Total of errors = ' in content:
            errors = content[content.find('Total of errors = '):]
            errors = errors[len('Total of errors = '):]
            e = ''
            for c in errors:
                if c.isdigit():
                    e += c
                else:
                    total_e = int(e)
                    break
        if 'Total of warnings = ' in content:
            errors = content[content.find('Total of warnings = '):]
            errors = errors[len('Total of warnings = '):]
            e = ''
            for c in errors:
                if c.isdigit():
                    e += c
                else:
                    total_w = int(e)
                    break
    else:
        total_f += 1
    return (total_f, total_e, total_w)


def dtd_validation(xml_filename, report_filename, doctype, database_name):
    if os.path.isfile(report_filename):
        os.unlink(report_filename)
    _use_packtools = (database_name == 'scielo')
    if _use_packtools:
        _use_packtools = IS_PACKTOOLS_INSTALLED
    if _use_packtools:
        return packtools_dtd_validation(xml_filename, report_filename)
    else:
        return java_xml_utils_dtd_validation(xml_filename, report_filename, doctype)


def style_validation(xml_filename, doctype, report_filename, xsl_prep_report, xsl_report, database_name):
    if os.path.isfile(report_filename):
        os.unlink(report_filename)
    _use_packtools = (database_name == 'scielo')
    if _use_packtools:
        _use_packtools = IS_PACKTOOLS_INSTALLED
    if _use_packtools:
        return packtools_style_validation(xml_filename, report_filename)
    else:
        return java_xml_utils_style_validation(xml_filename, doctype, report_filename, xsl_prep_report, xsl_report)


def validate_article_xml(xml_filename, dtd_files, dtd_report_filename, style_report_filename):
    register_log('validate_article_xml: inicio')
    is_valid_style = False

    register_log('validate_article_xml: inicio')
    xml, e = xml_utils.load_xml(xml_filename)
    is_valid_dtd = dtd_validation(xml_filename, dtd_report_filename, dtd_files.doctype_with_local_path, dtd_files.database_name)
    if e is None:
        is_valid_style = style_validation(xml_filename, dtd_files.doctype_with_local_path, style_report_filename, dtd_files.xsl_prep_report, dtd_files.xsl_report, dtd_files.database_name)
    else:
        text = 'FATAL ERROR: ' + _('Unable to load') + ' ' + xml_filename + '\n' + str(e).decode('utf-8')
        fs_utils.write_file(style_report_filename, text)
    f, e, w = style_checker_statistics(style_report_filename)
    register_log('validate_article_xml: fim')
    #open(os.path.dirname(style_report_filename) + '/validate_article_xml.log', 'a+').write('\n'.join(log_items))
    return (xml, is_valid_dtd, (f, e, w))
