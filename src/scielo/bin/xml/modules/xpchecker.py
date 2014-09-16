import os
from modules import java_xml_utils


def dtd_validation(xml_filename, report_filename):
    return java_xml_utils.xml_validate(xml_filename, report_filename, True)


def style_validation(xml_filename, report_filename, xsl_prep_report, xsl_report):
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
