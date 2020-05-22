# coding=utf-8
import os
from datetime import datetime

from ...__init__ import _
from ...generics import encoding
from ...generics import fs_utils
from ...generics import xml_utils

from ...generics.reports import validation_status
from ..pkg_processors import xml_versions


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
                self.dtd_files.data['dtd id'],
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


def dtd_locations():
    locations = {}
    for name, dtd_info in xml_versions.XPM_FILES.items():
        dtd_id = dtd_info.get('dtd id')
        if dtd_id not in locations.keys():
            locations[dtd_id] = {}
            locations[dtd_id] = [
                dtd_info.get('remote'),
                dtd_info.get('remote').replace('https:', 'http:')]
    return locations


class PackToolsXMLValidator(object):

    def __init__(self, file_path, tree, sps_version):
        self.file_path = file_path
        self.tree = tree
        self.sps_version = sps_version

        self.version = packtools.__version__

        self.xml_validator = None

    def validate_doctype(self):
        sps_version = self.sps_version
        public_id = self.tree.docinfo.public_id
        system_id = self.tree.docinfo.system_url
        if not sps_version:
            return []
        errors = []
        dtd_public_id_items = xml_versions.SPS_VERSIONS.get(sps_version)
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

        locations = dtd_locations().get(public_id)
        _location = None
        for location in locations:
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
        try:
            print(self.sps_version)
            self.xml_validator = packtools.XMLValidator.parse(
                    self.tree, sps_version=self.sps_version)
        except (packtools.etree.XMLSyntaxError, exceptions.XMLDoctypeError,
                exceptions.XMLSPSVersionError) as e:
            ERR_MESSAGE = ("Validation error of {}: {}.").format(
                self.file_path, e)
            dtd_errors = [ERR_MESSAGE]
            print(e)
        except exceptions.UndefinedDTDError as e:
            dtd_errors = [str(e)]
            print(e)
        else:
            print("validate_all()")
            dtd_is_valid, dtd_errors = self.xml_validator.validate_all()
            dtd_errors = xml_utils.format_validations_msg(dtd_errors)
            print(dtd_is_valid, dtd_errors)
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
