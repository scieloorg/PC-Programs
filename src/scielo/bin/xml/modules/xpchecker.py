import os


from modules import java_xml_utils


def packtools_dtd_validation(xml_filename, report_filename):
    from packtools import stylechecker
    print(xml_filename)
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


def java_xml_utils_dtd_validation(xml_filename, report_filename):
    return java_xml_utils.xml_validate(xml_filename, report_filename, True)


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


def dtd_validation(xml_filename, report_filename):
    return packtools_dtd_validation(xml_filename, report_filename)


def style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report):
    return packtools_style_validation(xml_filename, report_filename)
