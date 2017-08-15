# coding=utf-8
import os
from datetime import datetime

from ..__init__ import _
from . import fs_utils
from . import java_xml_utils
from . import xml_utils

from .reports import html_reports
from .reports import validation_status


IS_PACKTOOLS_INSTALLED = False
try:
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
except:
    os.environ['XML_CATALOG_FILES'] = ''


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


class PackToolsValidator(object):

    def __init__(self):
        pass

    def setup(self, xml_filename):
        import packtools
        self.xml_validator = packtools.stylechecker.XMLValidator(xml_filename)
        self.is_valid, self.errors = self.xml_validator.validate()

    def _save_style_report(self, content, report_filename):
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

        body = msg + ''.join([html_reports.display_xml(item) for item in content.split('\n')])
        html_reports.save(report_filename, title, body)

    @property
    def _dtd_validation(self):
        return '\n'.join([err.message for err in self.errors])

    def dtd_validation(self, report_filename):
        fs_utils.write_file(report_filename, self._dtd_validation)
        return self.is_valid

    @property
    def _style_validation(self):
        return xml_utils.etree.tostring(self.xml_validator.annotate_errors(), pretty_print=True, encoding='utf-8', xml_declaration=True)

    def style_validation(self, report_filename):
        self._save_style_report(self._style_validation, report_filename)
        f, e, w = style_checker_statistics(self._style_validation)
        return (f + e + w == 0)


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

    body = msg + ''.join([html_reports.display_xml(item) for item in content.split('\n')])
    html_reports.save(report_filename, title, body)


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

    def __init__(self, dtd_files):
        self.logger = None
        if dtd_files.database_name == 'scielo' and IS_PACKTOOLS_INSTALLED:
            self.validator = PackToolsValidator()
        else:
            self.validator = JavaXMLValidator(dtd_files.doctype_with_local_path, dtd_files.xsl_prep_report, dtd_files.xsl_report)

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
