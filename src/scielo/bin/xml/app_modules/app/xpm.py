# coding=utf-8

import os

from ..__init__ import _
from . import interface
from ..generics import encoding
from .data import workarea
from .data import package
from .pkg_processors import sgmlxml
from .pkg_processors import pkg_processors
from .config import config
from .pkg_processors import xml_versions


def call_make_packages(args, version):
    script, xml_path, acron, INTERATIVE, GENERATE_PMC = read_inputs(args)
    normalized_pkgfiles = None
    stage = 'xpm'
    if any([xml_path, acron]):
        result = validate_inputs(script, xml_path)
        if result is not None:
            sgm_xml, xml_list = result
            stage = 'xpm'
            normalized_pkgfiles = []
            if sgm_xml is not None:
                xml_generation = sgmlxml2xml(sgm_xml, acron)
                outputs = {xml_generation.xml_pkgfiles.name: xml_generation.sgmxml_outputs}
                normalized_pkgfiles = [xml_generation.xml_pkgfiles]
                stage = 'xml'
            else:
                normalized_pkgfiles, outputs = pkg_processors.normalize_xml_packages(xml_list, 'remote', stage)
    reception = XPM_Reception(stage, INTERATIVE)
    if normalized_pkgfiles is None:
        if INTERATIVE is True:
            reception.display_form()
    else:
        reception.make_package(normalized_pkgfiles, outputs, GENERATE_PMC)


def read_inputs(args):
    INTERATIVE = True
    GENERATE_PMC = False
    args = encoding.fix_args(args)
    script = args[0]
    path = None
    acron = None

    items = []
    for item in args:
        if item == '-auto':
            INTERATIVE = False
        elif item == '-pmc':
            GENERATE_PMC = True
        else:
            items.append(item)

    if len(items) == 3:
        script, path, acron = items
    elif len(items) == 2:
        script, path = items
    if path is not None:
        path = path.replace('\\', '/')
    return (script, path, acron, INTERATIVE, GENERATE_PMC)


def validate_inputs(script, xml_path):
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
        encoding.display_message('\n'.join(messages))
    else:
        return sgm_xml, xml_list


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


def sgmlxml2xml(sgm_xml_filename, acron):
    _sgmlxml2xml = sgmlxml.SGMLXML2SPSXMLConverter(xml_versions.xsl_getter)
    sgmxml_pkgfiles = workarea.PkgArticleFiles(sgm_xml_filename)
    pkg_generation = sgmlxml.SGMLXML2SPSXML(sgmxml_pkgfiles)
    pkg_generation.pack(acron, _sgmlxml2xml)
    return pkg_generation


class XPM_Reception(object):

    def __init__(self, stage, INTERATIVE=True):
        configuration = config.Configuration()
        self.proc = pkg_processors.PkgProcessor(configuration, INTERATIVE, stage)

    def display_form(self):
        interface.display_form(self.proc.stage == 'xc', None, self.call_make_package)

    def call_make_package(self, xml_path, GENERATE_PMC=False):
        encoding.display_message(_('Execute Make package') + ':')
        xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]
        encoding.display_message('Step 1/2 ...')
        normalized_pkgfiles, outputs = pkg_processors.normalize_xml_packages(xml_list, 'remote', self.proc.stage)
        encoding.display_message('Step 2/2 ...')
        self.make_package(normalized_pkgfiles, outputs, GENERATE_PMC)
        encoding.display_message('The End')
        return 'done', 'blue'

    def make_package(self, normalized_pkgfiles, outputs, GENERATE_PMC=False):
        if len(normalized_pkgfiles) > 0:
            workarea_path = os.path.dirname(normalized_pkgfiles[0].path)
            encoding.debugging('xpm.XPM_Reception.make_package - package.Package')
            pkg = package.Package(normalized_pkgfiles, outputs, workarea_path)
            encoding.debugging('xpm.XPM_Reception.make_package - proc.make_package')
            encoding.display_message(_('Making package') + ' ...')
            self.proc.make_package(pkg, GENERATE_PMC)
