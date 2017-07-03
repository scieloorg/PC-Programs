# coding=utf-8

import os
import sys

from ..__init__ import _
from . import interface
from ..useful import utils
from ..useful import fs_utils
from ..data import workarea
from ..pkg_processors import sgmlxml
from ..pkg_processors import pkg_processors


"""
from config import config
from ws import ws_requester
from ws import institutions_manager
configuration_filename = ' '
configuration = config.Configuration(configuration_filename)
app_ws_requester = ws_requester.WebServicesRequester(configuration.is_web_access_enabled, configuration.proxy_info)
app_institutions_manager = institutions_manager.InstitutionsManager(app_ws_requester)
"""


messages = []
xpm_process_logger = fs_utils.ProcessLogger()


def call_make_packages(args, version):
    script, path, acron, DISPLAY_REPORT, GENERATE_PMC = read_inputs(args)

    if path is None and acron is None:
        interface.open_main_window(False, None)
    else:
        sgm_xml, xml_list, errors = evaluate_inputs(path, acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python ' + script + ' <xml_src> [-auto]')
            messages.append(_('where') + ':')
            messages.append('  <xml_src> = ' + _('XML filename or path which contains XML files'))
            messages.append('  [-auto]' + _('optional parameter to omit report'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))
        else:
            stage = 'xpm'
            pkgfiles = []
            if sgm_xml is not None:
                pkgfiles = [sgmlxml2xml(sgm_xml, acron, version)]
                stage = 'xml'
            else:
                pkgfiles = pkg_processors.normalize_xml_packages(xml_list, stage)
            #validate_packages(pkgfiles, version, DISPLAY_REPORT, GENERATE_PMC, stage, sgm_xml)
            config = None
            db_manager = None
            proc = pkg_processors.PkgProcessor(config, version, DISPLAY_REPORT, GENERATE_PMC, db_manager, stage)
            proc.make_package([f.filename for f in pkgfiles])


def read_inputs(args):
    DISPLAY_REPORT = True
    GENERATE_PMC = False

    args = [arg.decode(encoding=sys.getfilesystemencoding()) for arg in args]
    script = args[0]
    path = None
    acron = None

    items = []
    for item in args:
        if item == '-auto':
            DISPLAY_REPORT = False
        elif item == '-pmc':
            GENERATE_PMC = True
        else:
            items.append(item)

    if len(items) == 3:
        script, path, acron = items
    elif len(items) == 2:
        script, path = items
    return (script, path, acron, DISPLAY_REPORT, GENERATE_PMC)


def evaluate_inputs(xml_path, acron):
    errors = []
    sgm_xml = None
    xml_list = None
    if xml_path is None:
        errors.append(_('Missing XML location. '))
    else:
        if os.path.isfile(xml_path):
            if xml_path.endswith('.sgm.xml'):
                sgm_xml = xml_path
            elif xml_path.endswith('.xml'):
                xml_list = [xml_path]
            else:
                errors.append(_('Invalid file. XML file required. '))
        elif os.path.isdir(xml_path):
            xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]
            if len(xml_list) == 0:
                errors.append(_('Invalid folder. Folder must have XML files. '))
        else:
            errors.append(_('Missing XML location. '))
    return sgm_xml, xml_list, errors


def sgmlxml2xml(sgm_xml_filename, acron, version):
    sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(version)
    pkgfiles = workarea.PackageFiles(sgm_xml_filename)
    wk = sgmlxml.SGMLXMLWorkarea(pkgfiles.name, pkgfiles.path)
    package_maker = sgmlxml.SGMLXML2SPSXMLPackageMaker(wk, pkgfiles)
    package_maker.pack(acron, sgmlxml2xml)
    return package_maker.xml_pkgfiles
