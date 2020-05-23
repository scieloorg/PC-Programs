# coding=utf-8
from __future__ import print_function, unicode_literals
import argparse
import logging
import logging.config
import os

from prodtools import _
from prodtools import form
from prodtools.config import config
from prodtools.processing.sgmlxml import SGMLXML2SPSXML
from prodtools.processing import pkg_processors
from prodtools.processing.sps_pkgmaker import PackageMaker


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


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
    if xml_list:
        execute(True, xml_list, GENERATE_PMC)
    else:
        display_form("xpm")
    return 'done', 'blue'


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


def requirements_checker():
    required = []
    try:
        from PIL import Image
    except ImportError:
        required.append('pillow')
    try:
        import packtools
    except ImportError:
        required.append('packtools')
    return required


def main():

    # xpm_version = pkg_resources.get_distribution('xpm').version

    parser = argparse.ArgumentParser(
        description='XML Package Maker cli utility')
    parser.add_argument(
        "xml_path", nargs="?", default='',
        help="filesystem path or URL to the XML")
    parser.add_argument(
        "acron", nargs="?", default='',
        help="journal acronym, required only for the conversion of SGML to XML"
    )
    parser.add_argument('--auto', action='store_true',
                        help='no user interface')

    parser.add_argument('--pmc', action='store_true',
                        help='generates also PMC package')

    parser.add_argument('--loglevel', default='WARNING')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    reqs = requirements_checker()
    if reqs:
        print('\n'.join(['not found: {}'.format(req) for req in reqs]))

    else:
        args = parser.parse_args()

        xml_path = args.xml_path
        acron = args.acron
        INTERATIVE = not args.auto
        GENERATE_PMC = args.pmc

        if not xml_path and INTERATIVE:
            display_form("xpm")
        else:
            sgmxml, xml_list, errors = evaluate_xml_path(xml_path)

            if sgmxml and not acron:
                errors.append(_('Inform the acron'))

            if errors:
                print("\n".join(errors))
                parser.print_usage()
                parser.print_help()
            else:
                execute(INTERATIVE, xml_list, GENERATE_PMC, sgmxml, acron)


if __name__ == '__main__':
    main()
