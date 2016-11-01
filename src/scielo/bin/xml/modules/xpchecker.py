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

import validation_status
import java_xml_utils
import xml_utils
import html_reports


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

    def finish(self):
        pass


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


class JavaXMLValidator(object):

    def __init__(self, doctype, xsl_prep_report, xsl_report):
        self.doctype = doctype
        self.xsl_prep_report = xsl_prep_report
        self.xsl_report = xsl_report
        self.logger = None

    def setup(self, xml_filename):
        self.xml_filename = xml_filename
        self.xml = java_xml_utils.XML(self.xml_filename, self.doctype)
        self.xml.logger = self.logger

    def dtd_validation(self, report_filename):
        return self.xml.xml_validate(report_filename)

    def style_validation(self, report_filename):
        is_valid_style = False
        xml_report = report_filename.replace('.html', '.xml')

        for item in [xml_report, report_filename]:
            if os.path.exists(item):
                os.unlink(item)

        parameters = {}
        if self.xml.transform_file(self.xsl_prep_report, xml_report, parameters):
            xml_transformer_report = java_xml_utils.XML(xml_report, None)
            xml_transformer_report.logger = self.logger
            xml_transformer_report.transform_file(self.xsl_report, report_filename, parameters)
            result = fs_utils.read_file(report_filename)
            if os.path.isfile(xml_report):
                os.unlink(xml_report)

        if not os.path.isfile(report_filename):
            result = 'ERROR: ' + _('Unable to create') + ' ' + report_filename
            fs_utils.write_file(report_filename, result)

        is_valid_style = ('Total of errors = 0' in result) and (('Total of warnings = 0' in result) or (not 'Total of warnings =' in result))

        return is_valid_style

    def finish(self):
        self.xml.finish()


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
        fs_utils.write_file(report_filename, validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to create') + ' ' + report_filename)
    if os.path.isfile(report_filename):
        c = fs_utils.read_file(report_filename)
        is_valid_style = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))

    if os.path.isfile(bkp_xml_filename):
        xml_utils.restore_xml_file(xml_filename, bkp_xml_filename)

    if os.path.isfile(xml_report):
        os.unlink(xml_report)
    register_log('java_xml_utils_style_validation: fim')
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
    is_valid_style = False

    register_log('validate_article_xml: inicio')
    xml, e = xml_utils.load_xml(xml_filename)
    is_valid_dtd = dtd_validation(xml_filename, dtd_report_filename, dtd_files.doctype_with_local_path, dtd_files.database_name)
    content = ''
    if e is None:
        is_valid_style = style_validation(xml_filename, dtd_files.doctype_with_local_path, style_report_filename, dtd_files.xsl_prep_report, dtd_files.xsl_report, dtd_files.database_name)
        content = fs_utils.read_file(style_report_filename)
    else:
        content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=xml_filename) + '\n' + e
        fs_utils.write_file(style_report_filename, content)
    f, e, w = style_checker_statistics(content)
    register_log('validate_article_xml: fim')
    #open(os.path.dirname(style_report_filename) + '/validate_article_xml.log', 'a+').write('\n'.join(log_items))
    return (xml, is_valid_dtd, (f, e, w))


class XMLValidator(object):

    def __init__(self, dtd_files):
        self.logger = None
        if dtd_files.database_name == 'scielo' and IS_PACKTOOLS_INSTALLED:
            self.validator = PackToolsValidator()
        else:
            self.validator = JavaXMLValidator(dtd_files.doctype_with_local_path, dtd_files.xsl_prep_report, dtd_files.xsl_report)

    def validate(self, xml_filename, dtd_report_filename, style_report_filename):
        self.logger.register('XMLValidator.validate - inicio')
        self.logger.register('XMLValidator.validate - self.validator.setup()')
        self.validator.logger = self.logger
        self.validator.setup(xml_filename)
        self.logger.register('XMLValidator.validate - xml_utils.load_xml')
        xml, e = xml_utils.load_xml(self.validator.xml.content)
        self.logger.register('XMLValidator.validate - self.validator.dtd_validation')
        is_valid_dtd = self.validator.dtd_validation(dtd_report_filename)
        content = ''
        if e is None:
            self.logger.register('XMLValidator.validate - self.validator.style_validation')
            self.validator.style_validation(style_report_filename)
            self.logger.register('XMLValidator.validate - fs_utils.read_file')
            content = fs_utils.read_file(style_report_filename)
        else:
            self.logger.register('XMLValidator.validate - e is not None')
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=xml_filename) + '\n' + e
            fs_utils.write_file(style_report_filename, content)
        self.logger.register('XMLValidator.validate - style_checker_statistics')
        f, e, w = style_checker_statistics(content)
        self.logger.register('XMLValidator.validate - self.validator.finish()')
        self.validator.finish()
        self.logger.register('XMLValidator.validate - fim')
        return (xml, is_valid_dtd, (f, e, w))
