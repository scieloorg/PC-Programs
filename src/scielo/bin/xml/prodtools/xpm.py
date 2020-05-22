# coding=utf-8
import logging
import logging.config

import os

from prodtools.utils import encoding
from prodtools import _
from prodtools import form
from prodtools.config import config
from prodtools.processing.sgmlxml import SGMLXML2SPSXML
from prodtools.processing import pkg_processors
from prodtools.processing.sps_pkgmaker import PackageMaker


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def call_make_packages(args, version):
    script, xml_path, acron, INTERATIVE, GENERATE_PMC = read_inputs(args)
    sgmxml = None
    xml_list = None
    if any([xml_path, acron]):
        result = validate_inputs(script, xml_path)
        if result:
            sgmxml, xml_list = result

    if sgmxml is None and xml_list is None:
        if INTERATIVE is True:
            display_form("xpm")
    else:
        execute(INTERATIVE, xml_list, GENERATE_PMC, sgmxml, acron)


def display_form(stage):
    form.display_form(stage == 'xc', None, call_make_package_from_form)


def execute(INTERATIVE, xml_list, GENERATE_PMC, sgmxml=None, acron=None):
    if xml_list:
        stage = 'xpm'
        xml_path = os.path.dirname(xml_list[0])
        pkg_maker = PackageMaker(xml_path, xml_path + "_" + stage)
        pkg = pkg_maker.pack(xml_list)
    elif sgmxml:
        stage = 'xml'
        logger.info("SGML to XML")
        sgmxml2xml = SGMLXML2SPSXML(sgmxml, acron)
        pkg = sgmxml2xml.pack()

    configuration = config.Configuration()
    proc = pkg_processors.PkgProcessor(configuration, INTERATIVE, stage)
    proc.make_package(pkg, stage == "xml" or GENERATE_PMC)
    print('...'*3)


def call_make_package_from_form(xml_path, GENERATE_PMC=False):
    xml_list = [os.path.join(xml_path, item)
                for item in os.listdir(xml_path) if item.endswith('.xml')]
    execute(True, xml_list, GENERATE_PMC)
    return 'done', 'blue'


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
            xml_list = [os.path.join(xml_path, item)
                        for item in os.listdir(xml_path)
                        if item.endswith('.xml')]

            if len(xml_list) == 0:
                errors.append(_('Invalid folder. Folder must have XML files. '))
        else:
            errors.append(_('Missing XML location. '))
    return sgm_xml, xml_list, errors
