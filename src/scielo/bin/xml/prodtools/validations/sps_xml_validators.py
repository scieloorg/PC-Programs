# coding=utf-8
import os
import logging
from datetime import datetime

from prodtools import _
from prodtools.utils import encoding
from prodtools.utils import fs_utils
from prodtools.utils import xml_utils
from prodtools.reports import validation_status
from prodtools.processing import xml_versions


IS_PACKTOOLS_INSTALLED = False
try:
    import packtools
    from packtools import exceptions
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
    IS_PACKTOOLS_INSTALLED = True
except Exception as e:
    print(e)
    os.environ['XML_CATALOG_FILES'] = ''


logger = logging.getLogger()


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


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


class PMCXMLValidator(object):

    def __init__(self, dtd_files, sps_version=None, preference=None):
        self.dtd_files = dtd_files

    def validate(self, xml_filename,
                 dtd_report_filename, style_report_filename):
        xml, valid = self.validate_structure(
            xml_filename, dtd_report_filename)
        f, e, w = self.validate_style(xml, style_report_filename)
        return (xml, valid, (f, e, w))

    def validate_structure(self, xml_filename, dtd_report_filename):
        xml_obj = xml_utils.get_xml_object(xml_filename)
        if not xml_obj:
            status = validation_status.STATUS_BLOCKING_ERROR
            content = "Unable to load {}".format(xml_filename)
        else:
            valid, errors = xml_utils.validate(
                xml_obj,
                self.dtd_files.data['dtd_id'],
                self.dtd_files.real_dtd_path)
            if errors:
                status = validation_status.STATUS_FATAL_ERROR
                content = "\n".join(errors)
                fs_utils.write_file(dtd_report_filename, content)
        content = "" if not status else status + '\n' + content + '\n' * 10
        fs_utils.write_file(dtd_report_filename, content)
        return xml_obj, valid

    def validate_style(self, xml_obj, report_filename):
        if os.path.isfile(report_filename):
            os.unlink(report_filename)
        transformed = None
        if xml_obj:
            transformed = xml_utils.transform(
                xml_obj, self.dtd_files.xsl_prep_report)
        if transformed:
            transformed = xml_utils.transform(
                transformed, self.dtd_files.xsl_report)
            xml_utils.write(report_filename, transformed)
            result = fs_utils.read_file(report_filename)
        if not os.path.isfile(report_filename):
            result = 'ERROR: ' + _('Unable to create') + ' ' + report_filename
            fs_utils.write_file(report_filename, result)
        return style_checker_statistics(result)


class PackToolsXMLValidator(object):

    def __init__(self, file_path, sps_version):
        self.file_path = file_path
        self.load_xml()
        self.sps_version = sps_version or xml_versions.get_latest_sps_version()

        self.version = packtools.__version__

        self.xml_validator = None
        self.locations = xml_versions.dtd_locations()

    def load_xml(self):
        content = fs_utils.read_file(self.file_path)
        content = xml_utils.insert_break_lines(content)
        self.tree, self.loading_error = xml_utils.load_xml(content)
        if self.loading_error:
            self.loading_error = (
                self.file_path + "\n\n" +
                self.loading_error + "\n\n" +
                xml_utils.numbered_lines(content)
            )
            fs_utils.write_file(self.file_path, content)

    def validate_doctype(self):
        sps_version = self.sps_version
        public_id = self.tree.docinfo.public_id
        system_id = self.tree.docinfo.system_url
        if not sps_version:
            return []
        errors = []
        dtd_public_id_items = xml_versions.SPS_VERSIONS.get(sps_version)
        if dtd_public_id_items is None:
            errors.append(
                _('{value} is an invalid value for {label}. ').format(
                    value=sps_version,
                    label='article/@specific-use')
                )
            return errors
        if public_id not in dtd_public_id_items:
            errors.append(
                _('{value} is an invalid value for {label}. ').format(
                    value=public_id or '',
                    label='DTD PUBLIC ID')
                )
            errors.append(
                _('{requirer} requires {required}. ').format(
                    requirer='SPS version {}'.format(sps_version),
                    required=_(" or ").join(dtd_public_id_items)
                ))
            return errors

        _location = None
        for location in self.locations.get(public_id):
            if system_id in location:
                _location = location
                break
        if not _location:
            errors.append(
                _('{value} is an invalid value for {label}. ').format(
                    value=system_id,
                    label='DTD SYSTEM ID')
            )
        return errors

    def validate_structure(self):
        dtd_is_valid = False
        dtd_errors = []
        if self.loading_error:
            dtd_errors = [self.loading_error]
            return dtd_is_valid, dtd_errors

        try:
            logger.info("sps_version: %s", self.sps_version)
            self.xml_validator = packtools.XMLValidator.parse(
                self.tree, sps_version=self.sps_version
            )
        except (packtools.etree.XMLSyntaxError, exceptions.XMLDoctypeError,
                exceptions.XMLSPSVersionError) as e:
            ERR_MESSAGE = ("Validation error of {}: {}.").format(
                self.file_path, e)
            dtd_errors = [ERR_MESSAGE]
            logger.error(e)
        except (exceptions.UndefinedDTDError, ValueError) as e:
            dtd_errors = [str(e)]
            logger.error(e)
        else:
            logger.debug("validate_all()")
            dtd_is_valid, dtd_errors = self.xml_validator.validate_all()
            dtd_errors = xml_utils.format_validations_msg(dtd_errors)
            logger.debug("dtd_is_valid: %s, dtd_errors: %s", dtd_is_valid, dtd_errors)

        return dtd_is_valid, dtd_errors

    def validate_style(self):
        if not self.xml_validator:
            return False, []
        sps_is_valid, sps_errors = self.xml_validator.validate_style()
        return sps_is_valid, sps_errors

    def annotated_errors(self):
        if self.xml_validator:
            content = packtools.etree.tostring(
                self.xml_validator.annotate_errors(),
                pretty_print=True,
                encoding='utf-8',
                xml_declaration=True)
            content = encoding.decode(content)
            return content
