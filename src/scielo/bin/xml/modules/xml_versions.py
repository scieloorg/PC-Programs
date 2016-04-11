# coding=utf-8
import os


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


DEFAULT_VERSION = '1.0'
PMC_PATH = THIS_LOCATION + '/../../pmc'

XSL_SGML2XML = {}
XSL_SGML2XML['3.0'] = PMC_PATH + '/v3.0/xsl/sgml2xml/sgml2xml.xsl'
XSL_SGML2XML['1.0'] = PMC_PATH + '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

DOCTYPE = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "http://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd">'

XPM_FILES = {}
XPM_FILES['scielo3.0'] = {}
XPM_FILES['scielo3.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_LOCAL_PATH}journalpublishing3.dtd">'
XPM_FILES['scielo3.0']['local'] = 'journalpublishing3.dtd'
XPM_FILES['scielo3.0']['remote'] = 'http://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd'
XPM_FILES['scielo3.0']['dtd_path'] = PMC_PATH + '/v3.0/dtd/'
XPM_FILES['scielo3.0']['css'] = PMC_PATH + '/v3.0/xsl/web/plus'
XPM_FILES['scielo3.0']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/scielo-style/stylechecker.xsl'
XPM_FILES['scielo3.0']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
XPM_FILES['scielo3.0']['xsl_preview'] = PMC_PATH + '/v3.0/xsl/previewers/scielo-html-novo.xsl'
XPM_FILES['scielo3.0']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/xml2pmc.xsl'

XPM_FILES['pmc3.0'] = {}
XPM_FILES['pmc3.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_LOCAL_PATH}journalpublishing3.dtd">'
XPM_FILES['pmc3.0']['local'] = 'journalpublishing3.dtd'
XPM_FILES['pmc3.0']['remote'] = 'http://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd'
XPM_FILES['pmc3.0']['dtd_path'] = PMC_PATH + '/v3.0/dtd'
XPM_FILES['pmc3.0']['css'] = PMC_PATH + '/v3.0/xsl/jpub/jpub-preview.css'
XPM_FILES['pmc3.0']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
XPM_FILES['pmc3.0']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
XPM_FILES['pmc3.0']['xsl_preview'] = [PMC_PATH + '/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
XPM_FILES['pmc3.0']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/pmc.xsl'

XPM_FILES['scielo1.0'] = {}
XPM_FILES['scielo1.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_LOCAL_PATH}JATS-journalpublishing1.dtd">'
XPM_FILES['scielo1.0']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.0']['remote'] = 'http://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd'
XPM_FILES['scielo1.0']['dtd_path'] = PMC_PATH + '/j1.0/dtd/jats1.0'
XPM_FILES['scielo1.0']['css'] = XPM_FILES['scielo3.0']['css']
XPM_FILES['scielo1.0']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/scielo-style/stylechecker.xsl'
XPM_FILES['scielo1.0']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.10/style-reporter.xsl'
XPM_FILES['scielo1.0']['xsl_preview'] = XPM_FILES['scielo3.0']['xsl_preview']
XPM_FILES['scielo1.0']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/xml2pmc.xsl'

XPM_FILES['pmc1.0'] = {}
XPM_FILES['pmc1.0']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_LOCAL_PATH}JATS-journalpublishing1.dtd">'
XPM_FILES['pmc1.0']['local'] = 'JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.0']['remote'] = 'http://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd'
XPM_FILES['pmc1.0']['dtd_path'] = PMC_PATH + '/j1.0/dtd/jats1.0'
XPM_FILES['pmc1.0']['css'] = XPM_FILES['pmc3.0']['css']
XPM_FILES['pmc1.0']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.10/nlm-stylechecker.xsl'
XPM_FILES['pmc1.0']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.10/style-reporter.xsl'
XPM_FILES['pmc1.0']['xsl_preview'] = [PMC_PATH + '/j1.0/xsl/jpub/citations-prep/jpub1-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
XPM_FILES['pmc1.0']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/pmc.xsl'


def xsl_sgml2xml(version):
    return XSL_SGML2XML.get(version, DEFAULT_VERSION)


class DTDFiles(object):

    def __init__(self, database_name, version):
        self.database_name = database_name
        self.version = version
        self.data = XPM_FILES.get(database_name + DEFAULT_VERSION, {})

    @property
    def doctype_with_local_path(self):
        return self.data['doctype'].replace('{DTD_LOCAL_PATH}', self.dtd_path + '/')

    @property
    def doctype(self):
        return self.data['doctype'].replace('{DTD_LOCAL_PATH}', '')

    @property
    def dtd_path(self):
        return self.data['dtd_path']

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
