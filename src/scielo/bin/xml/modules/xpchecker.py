import os

try:
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
except:
    os.environ['XML_CATALOG_FILES'] = ''

from modules import java_xml_utils
from modules import xml_utils


def packtools_dtd_validation(xml_filename, report_filename):
    from packtools import stylechecker
    xml_validator = stylechecker.XMLValidator(xml_filename)
    is_valid, errors = xml_validator.validate()
    r = '\n'.join([err.message for err in errors])
    open(report_filename, 'w').write(r)
    return is_valid


def packtools_style_validation(xml_filename, report_filename):
    from lxml import etree
    from packtools import stylechecker
    xml_validator = stylechecker.XMLValidator(xml_filename)
    is_valid, errors = xml_validator.validate()
    err_xml = xml_validator.annotate_errors()
    r = etree.tostring(err_xml, pretty_print=True, encoding='utf-8', xml_declaration=True)
    r = 'Total of errors = ' + str(len(errors)) + '\n' + r
    open(report_filename, 'w').write(r)
    return is_valid


def java_xml_utils_dtd_validation(xml_filename, report_filename, doctype):
    return java_xml_utils.xml_validate(xml_filename, report_filename, doctype)


def java_xml_utils_style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report):
    # STYLE CHECKER REPORT
    is_valid_style = False
    xml_report = report_filename.replace('.html', '.xml')
    if os.path.exists(xml_report):
        os.unlink(xml_report)
    if java_xml_utils.xml_transform(xml_filename, xsl_prep_report, xml_report):
        java_xml_utils.xml_transform(xml_report, xsl_report, report_filename)
    else:
        open(report_filename, 'w').write('FATAL ERROR: Unable to create ' + report_filename)
    if os.path.isfile(report_filename):
        c = open(report_filename, 'r').read()
        is_valid_style = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))

    if os.path.isfile(xml_report):
        os.unlink(xml_report)
    return is_valid_style


def dtd_validation(xml_filename, report_filename, doctype):
    #return packtools_dtd_validation(xml_filename, report_filename)
    return java_xml_utils_dtd_validation(xml_filename, report_filename, doctype)
    #try:
    #    return packtools_dtd_validation(xml_filename, report_filename)
    #except:
    #    return java_xml_utils_dtd_validation(xml_filename, report_filename, doctype)


def style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report):
    #return packtools_style_validation(xml_filename, report_filename)
    return java_xml_utils_style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report)

    #try:
    #    return packtools_style_validation(xml_filename, report_filename)
    #except:
    #    return java_xml_utils_dtd_validation(xml_filename, report_filename, xsl_prep_report, xsl_report)


def generate_validations_reports(xml_filename, dtd_files, dtd_validation_report_filename, style_checker_report_filename):
    xml = None
    is_valid_dtd = False
    is_valid_style = False
    e = None
    java_xml_utils.apply_dtd(xml_filename, dtd_files.doctype)
    if os.path.isfile(xml_filename):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)
        xml, e = xml_utils.load_xml(xml_filename)
        if e is None:
            is_valid_dtd = dtd_validation(xml_filename, dtd_validation_report_filename, dtd_files.doctype_with_local_path)
            is_valid_style = style_validation(xml_filename, style_checker_report_filename, dtd_files.xsl_prep_report, dtd_files.xsl_report)

    if xml is None:
        if e is None:
            e = ''
        open(dtd_validation_report_filename, 'w').write('Unable to load ' + xml_filename + '\n' + e)
        open(style_checker_report_filename, 'w').write('Unable to load ' + xml_filename + '\n' + e)

    return (xml, is_valid_dtd, is_valid_style)


def manage_validations_result(ctrl_filename, is_valid_dtd, is_valid_style, dtd_validation_report, style_checker_report):
    if ctrl_filename is None:
        if is_valid_style is True:
            os.unlink(style_checker_report)
    else:
        open(ctrl_filename, 'w').write('Finished')
    if os.path.isfile(dtd_validation_report):
        os.unlink(dtd_validation_report)


def validate_article_package(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename=None):
    # validation of scielo.xml
    loaded_xml, is_valid_dtd, is_valid_style = generate_validations_reports(xml_filename, dtd_files, dtd_report, style_report)

    if err_filename is not None:
        if os.path.isfile(dtd_report):
            open(err_filename, 'a+').write('\n\n\n' + '.........\n\n\n' + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(dtd_report, 'r').read())

    # manage result
    manage_validations_result(ctrl_filename, is_valid_dtd, is_valid_style, dtd_report, style_report)
    return (loaded_xml, is_valid_dtd, is_valid_style)


def validate_issue_package(xml_files, markup_xml_path, acron, version='1.0'):
    import files_manager
    import xml_versions

    do_toc_report = True

    scielo_pkg_path = markup_xml_path + '/scielo_package'
    pmc_pkg_path = markup_xml_path + '/pmc_package'
    report_path = markup_xml_path + '/errors'
    wrk_path = markup_xml_path + '/work'

    for d in [scielo_pkg_path, pmc_pkg_path, report_path]:
        if not os.path.isdir(d):
            os.makedirs(d)

    print('Validate packages (' + str(len(xml_files)) + '):')
    for xml_filename in xml_files:
        doc_files_info = files_manager.DocFilesInfo(xml_filename, report_path, wrk_path)
        doc_files_info.clean()

        dtd_files = xml_versions.DTDFiles('scielo', version)
        loaded_xml, is_valid_dtd, is_valid_style = validate_article_package(doc_files_info.new_xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)

        print(' ... validated')

    print('Generate contents validation reports...')
    reports.generate_package_reports(scielo_pkg_path, xml_names, report_path, do_toc_report)

