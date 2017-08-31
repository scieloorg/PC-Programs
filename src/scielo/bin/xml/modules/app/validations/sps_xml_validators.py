# coding=utf-8
import os
from datetime import datetime

from ...__init__ import _
from ...generics import encoding
from ...generics import fs_utils
from ...generics import java_xml_utils
from ...generics import xml_utils

from ...generics.reports import html_reports
from ...generics.reports import validation_status


IS_PACKTOOLS_INSTALLED = False
try:
    import packtools
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
    IS_PACKTOOLS_INSTALLED = True
except Exception as e:
    os.environ['XML_CATALOG_FILES'] = ''


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


class PackToolsValidator(object):

    def __init__(self, dtd_name, sps_version):
        self.xml_validator = None
        self.dtd_name = dtd_name
        self.dtd = packtools.etree.DTD(dtd_name)
        self.version = packtools.__version__
        self.is_valid = False
        self.style_errors = 0
        if sps_version in packtools.catalogs.SCH_SCHEMAS.keys():
            auto_loaded_sch_label = u'@' + sps_version
            self.style_validators = [
                    packtools.domain.SchematronValidator.from_catalog(
                        sps_version,
                        label=auto_loaded_sch_label),
                    packtools.domain.PyValidator(label=auto_loaded_sch_label),
                    # the python based validation pipeline
            ]
        self.annoted = None

    def setup(self, xml_filename):
        try:
            self.xml_validator = packtools.XMLValidator(
                                    packtools.etree.parse(xml_filename),
                                    dtd=self.dtd)
            self.xml_validator.style_validators = self.style_validators
            self.annotate_errors()
        except Exception as e:
            self.xml_validator = None

    def annotate_errors(self):
        if self.annoted is None:
            content = packtools.etree.tostring(
                self.xml_validator.annotate_errors(),
                pretty_print=True,
                encoding='utf-8',
                xml_declaration=True)
            content = encoding.decode(content)
            self.is_valid = True
            self.style_errors = content.count('SPS-ERROR')
            self.annoted = content

    def dtd_validation(self, report_filename):
        msg = 'Validates fine'
        if self.is_valid is False:
            msg = _('Invalid XML File')
        fs_utils.write_file(report_filename, msg)
        return self.is_valid

    def style_validation(self, report_filename):
        title = 'Packtools Style Checker (' + self.version + ')'
        header = ''
        if self.style_errors > 0:
            header = html_reports.tag('div', 'Total of errors = ' + str(self.style_errors), 'error')
        html = ''
        if self.annoted is not None:
            html = html_reports.display_xml(self.annoted)
            html = html.replace('&lt;!--', '<div style="background-color:#DCDCDC;color: red;"><em>&lt;!--').replace('--&gt;', '--&gt;</em></div>')
        html_reports.save(report_filename, title, header+html)
        return (self.style_errors == 0)


class JavaXMLValidator(object):

    def __init__(self, doctype, xsl_prep_report, xsl_report):
        self.doctype = doctype
        self.xsl_prep_report = xsl_prep_report
        self.xsl_report = xsl_report
        self.logger = None

    def setup(self, xml_filename):
        self.xml_filename = xml_filename

    def dtd_validation(self, report_filename):
        return java_xml_utils.xml_validate(self.xml_filename, report_filename, self.doctype)

    def style_validation(self, report_filename):
        is_valid_style = False
        xml_report = report_filename.replace('.html', '.xml')
        result = 'ERROR: ' + _('Unable to create') + ' ' + report_filename
        parameters = {}
        transformed = java_xml_utils.xml_transform(self.xml_filename, self.xsl_prep_report, xml_report, parameters)
        if transformed:
            transformed = java_xml_utils.xml_transform(xml_report, self.xsl_report, report_filename, parameters)
            result = fs_utils.read_file(report_filename)
            fs_utils.delete_file_or_folder(xml_report)
        if not os.path.isfile(report_filename):
            fs_utils.write_file(report_filename, result)
        is_valid_style = ('Total of errors = 0' in result) and (('Total of warnings = 0' in result) or (not 'Total of warnings =' in result))
        return is_valid_style


def style_checker_statistics(content):
    total_f = 0
    total_e = 0
    total_w = 0

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
    return (total_f, total_e, total_w)


class XMLValidator(object):

    def __init__(self, dtd_files, sps_version, preference):
        self.logger = None
        preference = preference[0] if preference is not None and len(preference) > 0 else ''
        if dtd_files.database_name == 'scielo' and IS_PACKTOOLS_INSTALLED and preference == 'packtools':
            self.validator = PackToolsValidator(dtd_files.local, sps_version)
            encoding.display_message('    XMLValidator: packtools')
        else:
            self.validator = JavaXMLValidator(dtd_files.doctype_with_local_path, dtd_files.xsl_prep_report, dtd_files.xsl_report)
            encoding.display_message('    XMLValidator: java')

    def validate(self, xml_filename, dtd_report_filename, style_report_filename):
        self.validator.logger = self.logger
        self.validator.setup(xml_filename)
        xml, e = xml_utils.load_xml(xml_filename)
        is_valid_dtd = self.validator.dtd_validation(dtd_report_filename)
        content = ''
        if e is None:
            self.validator.style_validation(style_report_filename)
            content = fs_utils.read_file(style_report_filename)
        else:
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=xml_filename) + '\n' + e
            fs_utils.write_file(style_report_filename, content)
        f, e, w = style_checker_statistics(content)
        return (xml, is_valid_dtd, (f, e, w))
