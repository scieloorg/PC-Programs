# coding=utf-8

import os
import sys

from ..__init__ import _
from . import interface
from ..generics import utils
from ..generics import encoding
from .data import workarea
from .data import package
from .pkg_processors import sgmlxml
from .pkg_processors import pkg_processors
from .config import config
from .pkg_processors import xml_versions


def call_make_packages(args, version):
    script, xml_path, acron, DISPLAY_REPORT, GENERATE_PMC = read_inputs(args)
    print(script, xml_path, acron, DISPLAY_REPORT, GENERATE_PMC)
    normalized_pkgfiles = None
    stage = 'xpm'
    if any([xml_path, acron]):
        stage, normalized_pkgfiles = get_normalized_pkgfiles(version, script, xml_path, acron)

    reception = XPM_Reception(version, stage, DISPLAY_REPORT)
    if normalized_pkgfiles is None:
        reception.display_form()
    else:
        reception.make_package(normalized_pkgfiles, GENERATE_PMC)


def get_normalized_pkgfiles(version, script, xml_path, acron):
    normalized_pkgfiles = None
    stage = 'xpm'
    sgm_xml, xml_list, errors = evaluate_xml_path(xml_path)
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
        normalized_pkgfiles = []
        if sgm_xml is not None:
            normalized_pkgfiles = [sgmlxml2xml(sgm_xml, acron, xml_versions.xsl_sgml2xml(version))]
            stage = 'xml'
        else:
            normalized_pkgfiles = pkg_processors.normalize_xml_packages(xml_list, 'remote', stage)
    return stage, normalized_pkgfiles


def read_inputs(args):
    DISPLAY_REPORT = True
    GENERATE_PMC = False

    args = [encoding.decode(arg, sys.getfilesystemencoding()) for arg in args]
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


def evaluate_xml_path(xml_path):
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


def sgmlxml2xml(sgm_xml_filename, acron, xsl):
    _sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(xsl)
    pkgfiles = workarea.PackageFiles(sgm_xml_filename)
    wk = sgmlxml.SGMLXMLWorkarea(pkgfiles.name, pkgfiles.path)
    package_maker = sgmlxml.SGMLXML2SPSXMLPackageMaker(wk, pkgfiles)
    package_maker.pack(acron, _sgmlxml2xml)
    return package_maker.xml_pkgfiles


class XPM_Reception(object):

    def __init__(self, version, stage, DISPLAY_REPORT=True):
        configuration = config.Configuration()
        self.proc = pkg_processors.PkgProcessor(configuration, version, DISPLAY_REPORT, stage)

    def display_form(self):
        interface.display_form(self.proc.stage == 'xc', None, self.call_make_package)

    def call_make_package(self, xml_path, GENERATE_PMC=False):
        xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]
        normalized_pkgfiles = pkg_processors.normalize_xml_packages(xml_list, (self.proc.scielo_dtd_files.local, self.proc.scielo_dtd_files.remote), self.proc.stage)
        self.make_package(normalized_pkgfiles, GENERATE_PMC)
        return 'done', 'blue'

    def make_package(self, normalized_pkgfiles, GENERATE_PMC=False):
        if len(normalized_pkgfiles) > 0:
            files = [f.filename for f in normalized_pkgfiles]
            workarea_path = os.path.dirname(normalized_pkgfiles[0].path)
            print('make_package', workarea_path)
            pkg = package.Package(files, workarea_path)
            self.proc.make_package(pkg, GENERATE_PMC)
