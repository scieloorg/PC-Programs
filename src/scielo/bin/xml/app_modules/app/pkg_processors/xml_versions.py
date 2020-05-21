# coding=utf-8
import os

from ...__init__ import PMC_PATH
from ...__init__ import BIN_XML_PATH
from ...__init__ import RELATIVE_PMC_PATH
from ...__init__ import INVALID_APP_PATH


JAVA_PATH = 'java'
_PMC_PATH = PMC_PATH

if INVALID_APP_PATH:
    if not os.path.isdir(RELATIVE_PMC_PATH):
        os.chdir(BIN_XML_PATH)
        if os.path.isdir(RELATIVE_PMC_PATH):
            _PMC_PATH = RELATIVE_PMC_PATH


DEFAULT_VERSION = '1.1'

valid_dtd_items = ['3.0', '1.0', 'j1.0', 'j1.1']

XSL_SGML2XML = {}
XSL_SGML2XML['3.0'] = os.path.join(PMC_PATH, 'v3.0/xsl/sgml2xml/sgml2xml.xsl')
XSL_SGML2XML['1.0'] = os.path.join(PMC_PATH, 'j1.0/xsl/sgml2xml/sgml2xml.xsl')
XSL_SGML2XML['1.1'] = os.path.join(PMC_PATH, 'j1.1/xsl/sgml2xml/sgml2xml.xsl')

XPM_FILES = {}
XPM_FILES['scielo3.0'] = {}
XPM_FILES['scielo3.0']['dtd id'] = '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN'
XPM_FILES['scielo3.0']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['scielo3.0']['dtd id'] + '" "{DTD_LOCAL_PATH}/journalpublishing3.dtd">'
XPM_FILES['scielo3.0']['local'] = 'journalpublishing3.dtd'
XPM_FILES['scielo3.0']['remote'] = 'https://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd'
XPM_FILES['scielo3.0']['dtd_path'] = os.path.join(PMC_PATH, 'v3.0/dtd')
XPM_FILES['scielo3.0']['relative_dtd_path'] = os.path.join(PMC_PATH, 'v3.0/dtd')
XPM_FILES['scielo3.0']['css'] = os.path.join(PMC_PATH, 'v3.0/xsl/web/plus')
XPM_FILES['scielo3.0']['xsl_prep_report'] = os.path.join(PMC_PATH, 'v3.0/xsl/scielo-style/stylechecker.xsl')
XPM_FILES['scielo3.0']['xsl_report'] = os.path.join(PMC_PATH, 'v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl')
XPM_FILES['scielo3.0']['xsl_preview'] = os.path.join(PMC_PATH, 'v3.0/xsl/previewers/scielo-html-novo.xsl')
XPM_FILES['scielo3.0']['xsl_output'] = os.path.join(PMC_PATH, 'v3.0/xsl/sgml2xml/xml2pmc.xsl')

XPM_FILES['pmc3.0'] = {}
XPM_FILES['pmc3.0']['dtd id'] = '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN'
XPM_FILES['pmc3.0']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['pmc3.0']['dtd id'] + '" "{DTD_LOCAL_PATH}/journalpublishing3.dtd">'
XPM_FILES['pmc3.0']['local'] = 'journalpublishing3.dtd'
XPM_FILES['pmc3.0']['remote'] = 'https://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd'
XPM_FILES['pmc3.0']['dtd_path'] = os.path.join(PMC_PATH, 'v3.0/dtd')
XPM_FILES['pmc3.0']['relative_dtd_path'] = os.path.join(PMC_PATH, 'v3.0/dtd')
XPM_FILES['pmc3.0']['css'] = os.path.join(PMC_PATH, 'v3.0/xsl/jpub/jpub-preview.css')
XPM_FILES['pmc3.0']['xsl_prep_report'] = os.path.join(PMC_PATH, 'v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl')
XPM_FILES['pmc3.0']['xsl_report'] = os.path.join(PMC_PATH, 'v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl')
XPM_FILES['pmc3.0']['xsl_preview'] = [os.path.join(PMC_PATH, 'v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl'), os.path.join(PMC_PATH, 'v3.0/xsl/previewers/jpub-main-jpub3-html.xsl'), ]
XPM_FILES['pmc3.0']['xsl_output'] = os.path.join(PMC_PATH, 'v3.0/xsl/sgml2xml/pmc.xsl')

XPM_FILES['scielo1.0'] = {}
XPM_FILES['scielo1.0']['dtd id'] = '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN'
XPM_FILES['scielo1.0']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['scielo1.0']['dtd id'] + '" "{DTD_LOCAL_PATH}/JATS-journalpublishing1.dtd">'
XPM_FILES['scielo1.0']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.0']['remote'] = 'https://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.0']['dtd_path'] = os.path.join(PMC_PATH, 'j1.0/dtd/jats1.0')
XPM_FILES['scielo1.0']['relative_dtd_path'] = os.path.join(PMC_PATH, 'j1.0/dtd/jats1.0')
XPM_FILES['scielo1.0']['css'] = XPM_FILES['scielo3.0']['css']
XPM_FILES['scielo1.0']['xsl_prep_report'] = os.path.join(PMC_PATH, 'j1.0/xsl/scielo-style/stylechecker.xsl')
XPM_FILES['scielo1.0']['xsl_report'] = os.path.join(PMC_PATH, 'j1.0/xsl/nlm-style-5.13/style-reporter.xsl')
XPM_FILES['scielo1.0']['xsl_preview'] = XPM_FILES['scielo3.0']['xsl_preview']
XPM_FILES['scielo1.0']['xsl_output'] = os.path.join(PMC_PATH, 'j1.0/xsl/sgml2xml/xml2pmc.xsl')

XPM_FILES['pmc1.0'] = {}
XPM_FILES['pmc1.0']['dtd id'] = '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN'
XPM_FILES['pmc1.0']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['pmc1.0']['dtd id'] + '" "{DTD_LOCAL_PATH}/JATS-journalpublishing1.dtd">'
XPM_FILES['pmc1.0']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.0']['remote'] = 'https://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.0']['dtd_path'] = os.path.join(PMC_PATH, 'j1.0/dtd/jats1.0')
XPM_FILES['pmc1.0']['relative_dtd_path'] = os.path.join(PMC_PATH, 'j1.0/dtd/jats1.0')
XPM_FILES['pmc1.0']['css'] = XPM_FILES['pmc3.0']['css']
XPM_FILES['pmc1.0']['xsl_prep_report'] = os.path.join(PMC_PATH, 'j1.0/xsl/nlm-style-5.13/nlm-stylechecker.xsl')
XPM_FILES['pmc1.0']['xsl_report'] = os.path.join(PMC_PATH, 'j1.0/xsl/nlm-style-5.13/style-reporter.xsl')
XPM_FILES['pmc1.0']['xsl_preview'] = [os.path.join(PMC_PATH, 'j1.0/xsl/jpub/citations-prep/jpub1-PMCcit.xsl'), os.path.join(PMC_PATH, 'v3.0/xsl/previewers/jpub-main-jpub3-html.xsl'), ]
XPM_FILES['pmc1.0']['xsl_output'] = os.path.join(PMC_PATH, 'j1.0/xsl/sgml2xml/pmc.xsl')

XPM_FILES['scielo1.1'] = {}
XPM_FILES['scielo1.1']['dtd id'] = '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN'
XPM_FILES['scielo1.1']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['scielo1.1']['dtd id'] + '" "{DTD_LOCAL_PATH}/JATS-journalpublishing1.dtd">'
XPM_FILES['scielo1.1']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.1']['remote'] = 'https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.1']['dtd_path'] = os.path.join(PMC_PATH, 'j1.1/JATS-Publishing-1-1-MathML2-DTD/JATS-Publishing-1-1-MathML2-DTD')
XPM_FILES['scielo1.1']['relative_dtd_path'] = os.path.join(PMC_PATH, 'j1.1/JATS-Publishing-1-1-MathML2-DTD/JATS-Publishing-1-1-MathML2-DTD')
XPM_FILES['scielo1.1']['css'] = XPM_FILES['scielo3.0']['css']
XPM_FILES['scielo1.1']['xsl_prep_report'] = os.path.join(PMC_PATH, 'j1.1/xsl/scielo-style/stylechecker.xsl')
XPM_FILES['scielo1.1']['xsl_report'] = os.path.join(PMC_PATH, 'j1.1/xsl/nlm-style-5.25/style-reporter.xsl')
XPM_FILES['scielo1.1']['xsl_preview'] = XPM_FILES['scielo3.0']['xsl_preview']
XPM_FILES['scielo1.1']['xsl_output'] = os.path.join(PMC_PATH, 'j1.1/xsl/sgml2xml/xml2pmc.xsl')

XPM_FILES['pmc1.1'] = {}
XPM_FILES['pmc1.1']['dtd id'] = '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN'
XPM_FILES['pmc1.1']['doctype'] = '<!DOCTYPE article PUBLIC "' + XPM_FILES['pmc1.1']['dtd id'] + '" "{DTD_LOCAL_PATH}/JATS-journalpublishing1.dtd">'
XPM_FILES['pmc1.1']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.1']['remote'] = 'https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.1']['dtd_path'] = os.path.join(PMC_PATH, 'j1.1/JATS-Publishing-1-1-MathML2-DTD/JATS-Publishing-1-1-MathML2-DTD')
XPM_FILES['pmc1.1']['relative_dtd_path'] = os.path.join(PMC_PATH, 'j1.1/JATS-Publishing-1-1-MathML2-DTD/JATS-Publishing-1-1-MathML2-DTD')
XPM_FILES['pmc1.1']['css'] = XPM_FILES['pmc3.0']['css']
XPM_FILES['pmc1.1']['xsl_prep_report'] = os.path.join(PMC_PATH, 'j1.1/xsl/nlm-style-5.25/nlm-stylechecker.xsl')
XPM_FILES['pmc1.1']['xsl_report'] = os.path.join(PMC_PATH, 'j1.1/xsl/nlm-style-5.25/style-reporter.xsl')
XPM_FILES['pmc1.1']['xsl_preview'] = [os.path.join(PMC_PATH, 'j1.1/xsl/jpub/citations-prep/jpub1-PMCcit.xsl'), os.path.join(PMC_PATH, 'v3.0/xsl/previewers/jpub-main-jpub3-html.xsl'), ]
XPM_FILES['pmc1.1']['xsl_output'] = os.path.join(PMC_PATH, 'j1.1/xsl/sgml2xml/pmc.xsl')


_SPS_VERSIONS = (
    ('None', [
        '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
    ]),
    ('sps-1.0', [
        '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
    ]),
    ('sps-1.1', [
        '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
    ]),
    ('sps-1.2', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    ]),
    ('sps-1.3', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    ]),
    ('sps-1.4', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    ]),
    ('sps-1.5', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    ]),
    ('sps-1.6', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    ]),
    ('sps-1.7', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
    ]),
    ('sps-1.8', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
    ]),
    ('sps-1.9', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
    ]),
)
SPS_VERSIONS = dict(_SPS_VERSIONS)


def get_dtd_version(sps_version_number):
    if not sps_version_number:
        return '3.0'
    elif float(sps_version_number) < 1.7:
        return '1.0'
    else:
        return '1.1'


def xsl_getter(sps_version_number):
    if not sps_version_number:
        return XSL_SGML2XML.get(DEFAULT_VERSION)
    dtd_version = get_dtd_version(sps_version_number)
    return XSL_SGML2XML.get(dtd_version, XSL_SGML2XML.get(DEFAULT_VERSION))


def dtd_location(xml):
    for name, data in XPM_FILES.items():
        if data.get('dtd id') in xml:
            return data.get('local'), data.get('remote')
    data = XPM_FILES['scielo'+DEFAULT_VERSION]
    return data.get('local'), data.get('remote')


def dtd_files(sps_version_number, database='scielo'):
    dtd_version = get_dtd_version(sps_version_number)
    return DTDFiles(database, dtd_version)


class DTDFiles(object):

    def __init__(self, database_name, version):
        self.database_name = database_name
        self.version = version
        self.data = XPM_FILES.get(database_name + version, XPM_FILES.get(database_name + DEFAULT_VERSION))

    @property
    def doctype_with_local_path(self):
        return self.data['doctype'].replace('{DTD_LOCAL_PATH}', self.relative_dtd_path)

    @property
    def doctype_with_remote_path(self):
        return self.data['doctype'].replace('{DTD_LOCAL_PATH}', self.remote)

    @property
    def doctype(self):
        return self.data['doctype'].replace('{DTD_LOCAL_PATH}', '')

    @property
    def real_dtd_path(self):
        return os.path.join(self.data['dtd_path'], self.data['local'])

    @property
    def dtd_path(self):
        return self.data['dtd_path']

    @property
    def relative_dtd_path(self):
        return self.data['relative_dtd_path']

    @property
    def xsl_prep_report(self):
        return self.data['xsl_prep_report']

    @property
    def xsl_report(self):
        return self.data['xsl_report']

    @property
    def xsl_output(self):
        return self.data['xsl_output']

    @property
    def local(self):
        return self.data['local']

    @property
    def remote(self):
        return self.data['remote']
