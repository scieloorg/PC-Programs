import os

try:
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
except:
    os.environ['XML_CATALOG_FILES'] = ''

import java_xml_utils
import xml_utils
import report_html
import files_manager
import xml_versions


def html_packtools_style_report(content, report_filename):
    version = ''
    try:
        import pkg_resources
        version = pkg_resources.get_distribution('packtools').version
    except:
        pass

    reporthtml = report_html.ReportHTML()
    q = len(content.split('SPS-ERROR')) - 1

    reporthtml.title = 'Style Checker (packtools' + version + ')'
    if q > 0:
        msg = reporthtml.tag('div', 'Total of errors = ' + str(q), 'error')

    reporthtml.body = msg + reporthtml.display_xml(content)
    reporthtml.save(report_filename)


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
    html_packtools_style_report(r, report_filename)
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


def dtd_validation(xml_filename, report_filename, doctype, database_name):
    if database_name == 'scielo':
        try:
            return packtools_dtd_validation(xml_filename, report_filename)
        except Exception as e:
            print(e)
            return java_xml_utils_dtd_validation(xml_filename, report_filename, doctype)
    else:
        return java_xml_utils_dtd_validation(xml_filename, report_filename, doctype)


def style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report, database_name):
    if database_name == 'scielo':
        try:
            return packtools_style_validation(xml_filename, report_filename)
        except Exception as e:
            print(e)
            return java_xml_utils_style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report)
    else:
        return java_xml_utils_style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report)


def generate_xml_validations_reports(xml_filename, dtd_files, dtd_validation_report_filename, style_checker_report_filename):
    xml = None
    is_valid_dtd = False
    is_valid_style = False
    e = None
    java_xml_utils.apply_dtd(xml_filename, dtd_files.doctype)
    if os.path.isfile(xml_filename):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)
        xml, e = xml_utils.load_xml(xml_filename)
        if e is None:
            is_valid_dtd = dtd_validation(xml_filename, dtd_validation_report_filename, dtd_files.doctype_with_local_path, dtd_files.database_name)
            is_valid_style = style_validation(xml_filename, style_checker_report_filename, dtd_files.xsl_prep_report, dtd_files.xsl_report, dtd_files.database_name)

    if xml is None:
        if e is None:
            e = ''
        open(dtd_validation_report_filename, 'w').write('Unable to load ' + xml_filename + '\n' + e)
        open(style_checker_report_filename, 'w').write('Unable to load ' + xml_filename + '\n' + e)

    return (xml, is_valid_dtd, is_valid_style)


def delete_exceding_reports(ctrl_filename, is_valid_dtd, is_valid_style, dtd_validation_report, style_checker_report):
    if ctrl_filename is None:
        if is_valid_style is True:
            os.unlink(style_checker_report)
    else:
        open(ctrl_filename, 'w').write('Finished')
    if os.path.isfile(dtd_validation_report):
        os.unlink(dtd_validation_report)


def validate_article_xml(xml_filename, dtd_files, dtd_report, style_report, ctrl_filename, err_filename=None):
    # validation of scielo.xml
    loaded_xml, is_valid_dtd, is_valid_style = generate_xml_validations_reports(xml_filename, dtd_files, dtd_report, style_report)

    if err_filename is not None:
        if os.path.isfile(dtd_report):
            open(err_filename, 'a+').write('\n\n\n' + '.........\n\n\n' + 'DTD errors\n' + '-'*len('DTD errors') + '\n' + open(dtd_report, 'r').read())

    # manage result
    delete_exceding_reports(ctrl_filename, is_valid_dtd, is_valid_style, dtd_report, style_report)
    return (loaded_xml, is_valid_dtd, is_valid_style)


def validate_issue_package(xml_files, report_path, wrk_path, version):
    print('Validate XML files')
    for xml_filename in xml_files:
        print('validating: ' + os.path.basename(xml_filename))
        doc_files_info = files_manager.DocumentFiles(xml_filename, report_path, wrk_path)
        doc_files_info.clean()

        dtd_files = xml_versions.DTDFiles('scielo', version)
        loaded_xml, is_valid_dtd, is_valid_style = validate_article_xml(xml_filename, dtd_files, doc_files_info.dtd_report_filename, doc_files_info.style_report_filename, doc_files_info.ctrl_filename, doc_files_info.err_filename)
