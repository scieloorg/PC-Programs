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
from ..pkg_processors import xml_versions
from . import data_validations


IS_PACKTOOLS_INSTALLED = False
try:
    import packtools
    from packtools.catalogs import XML_CATALOG
    from packtools import exceptions
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
        self.xml_validator = None
        self.is_valid = False
        self.style_errors = 1
        try:
            parsed_xml = packtools.XML(xml_filename)
            self.xml_validator = packtools.XMLValidator.parse(parsed_xml)
            self.annotate_errors()
        except (packtools.etree.XMLSyntaxError, exceptions.XMLDoctypeError,
                exceptions.XMLSPSVersionError) as e:
            ERR_MESSAGE = "Something went wrong while working on {filename}: {details}."
            self.annoted = ERR_MESSAGE.format(filename=xml_filename, details=e)

    def annotate_errors(self):
        if self.annoted is None:
            """
            summary = {
                'dtd_errors': [_make_err_message(err) for err in dtd_errors],
                'style_errors': {},
                'is_valid': bool(dtd_is_valid and sps_is_valid),
            }
            """
            content = packtools.etree.tostring(
                self.xml_validator.annotate_errors(),
                pretty_print=True,
                encoding='utf-8',
                xml_declaration=True)
            content = encoding.decode(content)
            self.annoted = content
            encoding.debugging('XML_CATALOG_FILES', os.environ['XML_CATALOG_FILES'])
            dtd_is_valid, dtd_errors = True, []
            try:
                dtd_is_valid, dtd_errors = self.xml_validator.validate()
            except Exception as e:
                encoding.report_exception('PackToolsValidator.annotate_errors', e, 'validate()')
            sps_is_valid, sps_errors = True, []
            try:
                sps_is_valid, sps_errors = self.xml_validator.validate_style()
            except Exception as e:
                encoding.report_exception('PackToolsValidator.annotate_errors', e, 'validate_style()')
            self.is_valid = bool(dtd_is_valid and sps_is_valid)
            self.style_errors = len(dtd_errors) + len(sps_errors)

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

    def __init__(self, dtd_files, sps_version=None, preference=None):
        self.logger = None
        self.SPS_versions = SPSversions()
        self.dtd_files = dtd_files
        self.dtd_validator = JavaXMLValidator(dtd_files.doctype_with_local_path, dtd_files.xsl_prep_report, dtd_files.xsl_report)
        validator_id = 'java'
        preference = preference[0] if preference is not None and len(preference) > 0 else ''
        if dtd_files.database_name == 'scielo' and IS_PACKTOOLS_INSTALLED and preference == 'packtools':
            try:
                self.validator = PackToolsValidator(
                    dtd_files.local, sps_version)
                encoding.display_message('    XMLValidator: packtools')
                validator_id = 'packtools'
            except Exception as e:
                encoding.report_exception('XMLValidator.__init__', e, dtd_files.local)
        if validator_id == 'java':
            self.validator = self.dtd_validator
            encoding.display_message('    XMLValidator: java')

    def validate_doctype(self, article_xml_versions_info):
        errors = []
        print(article_xml_versions_info.public_id,
            article_xml_versions_info.system_id,
            article_xml_versions_info.sps_version)
        info = self.SPS_versions.dtd_infos.get(
            article_xml_versions_info.public_id)
        if info is not None:
            if article_xml_versions_info.system_id not in info.get('url'):
                expected = _(' or ').join(info.get('url'))
                msg = data_validations.invalid_value_message(
                    'SYSTEM ID', article_xml_versions_info.system_id, expected)
                errors.append(msg)
            if article_xml_versions_info.sps_version not in info.get('sps'):
                expected = _(' or ').join(info.get('sps'))
                msg = data_validations.invalid_value_message(
                    'SPS version', article_xml_versions_info.sps_version, expected)
                errors.append(msg)
        else:
            errors.append(_('Unknown PUBLIC ID: {}').format(
                article_xml_versions_info.public_id))
        if len(errors) > 0:
            errors.insert(0, 'PUBLIC ID: {}'.format(
                article_xml_versions_info.public_id))
        return errors

    def validate(self, xml_filename, dtd_report_filename, style_report_filename):
        self.dtd_validator.logger = self.logger
        self.dtd_validator.setup(xml_filename)
        self.validator.logger = self.logger
        self.validator.setup(xml_filename)
        xml, e = xml_utils.load_xml(xml_filename)
        errors = []
        if self.dtd_files.database_name == 'scielo':
            errors = self.validate_doctype(ArticleXMLVersionsInfo(fs_utils.read_file(xml_filename)))
        is_valid_dtd = self.dtd_validator.dtd_validation(dtd_report_filename)
        is_valid_dtd = len(errors) == 0 and is_valid_dtd
        if len(errors) > 0:
            dtd_report_content = fs_utils.read_file(dtd_report_filename)
            if dtd_report_content is None:
                dtd_report_content = ''
            fs_utils.write_file(
                dtd_report_filename,
                '\n'.join(errors) + '\n' + dtd_report_content)
        content = ''
        if e is None:
            self.validator.style_validation(style_report_filename)
            content = fs_utils.read_file(style_report_filename)
        else:
            content = validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=xml_filename) + '\n' + e
            try:
                content += e
            except:
                pass
            fs_utils.write_file(style_report_filename, content)
        f, e, w = style_checker_statistics(content)
        return (xml, is_valid_dtd, (f, e, w))


class ArticleXMLVersionsInfo(object):

    def __init__(self, xml_content):
        self.xml_content = xml_content
        self._DOCTYPE = None
        self._public_id = None
        self._system_id = None
        self._sps_version = None

    @property
    def DOCTYPE(self):
        if self._DOCTYPE is None:
            if '<!DOCTYPE' in self.xml_content:
                self._DOCTYPE = self.xml_content[self.xml_content.find('<!DOCTYPE'):]
                self._DOCTYPE = self._DOCTYPE[:self._DOCTYPE.find('>')+1]
        return self._DOCTYPE

    @property
    def public_id(self):
        if self._public_id is None:
            if self.DOCTYPE is not None:
                self._public_id = self.DOCTYPE[self.DOCTYPE.find('"')+1:]
                self._public_id = self._public_id[:self._public_id.find('"')]
        return self._public_id

    @property
    def system_id(self):
        if self._system_id is None:
            if 'http' in self.DOCTYPE:
                self._system_id = self.DOCTYPE[self.DOCTYPE.find('"http')+1:]
                self._system_id = self._system_id[:self._system_id.find('"')]
        return self._system_id

    @property
    def sps_version(self):
        if self._sps_version is None:
            if '<article' in self.xml_content:
                elem = self.xml_content[self.xml_content.find('<article'):]
                elem = elem[:elem.find('>')]
                if 'specific-use="' in elem:
                    self._sps_version = elem[elem.find('specific-use="')+len('specific-use="'):]
                    self._sps_version = self._sps_version[:self._sps_version.find('"')]
        return str(self._sps_version)


class SPSversions(object):

    def __init__(self):
        self.versions = {}
        self.dtd_infos = {}
        self.dtd_id_items = [
            '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
        ]
        self.versions[self.dtd_id_items[0]] = [
            'None',
            'sps-1.0',
            'sps-1.1',
            ]
        self.versions[self.dtd_id_items[1]] = [
            'sps-1.2',
            'sps-1.3',
            'sps-1.4',
            'sps-1.5',
            'sps-1.6',
            'sps-1.7',
            ]
        self.versions[self.dtd_id_items[2]] = [
            'sps-1.7',
            ]

        for name, dtd_info in xml_versions.XPM_FILES.items():
            dtd_id = dtd_info.get('dtd id')
            if dtd_id not in self.dtd_infos.keys():
                self.dtd_infos[dtd_id] = {}
            self.dtd_infos[dtd_id]['url'] = [
                dtd_info.get('remote'),
                dtd_info.get('remote').replace('https:', 'http:')]
            self.dtd_infos[dtd_id]['sps'] = self.versions.get(dtd_id)
