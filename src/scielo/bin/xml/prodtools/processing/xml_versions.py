# coding=utf-8
import os

from prodtools import DTD_AND_XSL_PATH

import configparser

XPM_FILES = configparser.ConfigParser()
XPM_FILES.read(os.path.join(DTD_AND_XSL_PATH, 'versions.ini'))


DEFAULT_VERSION = XPM_FILES.sections()[0]

valid_dtd_items = XPM_FILES.sections()

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
    ('sps-1.10', [
      '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
    ]),
)
SPS_VERSIONS = dict(_SPS_VERSIONS)


def get_latest_sps_version():
    return _SPS_VERSIONS[-1][0]


def sps_numbers(sps: str) -> tuple:
    if sps and 'sps-' in sps:
        sps = sps[4:]
    try:
        numbers = [int(n) for n in sps.split(".")]
    except (AttributeError, ValueError, TypeError):
        return (0, 0)
    else:
        return tuple(numbers)


def get_dtd_version(sps_version):
    print("DTD version: %s" % sps_version)
    numbers = sps_numbers(sps_version)
    if numbers == (0, 0):
        return '3.0'
    elif numbers < (1, 7):
        return 'j1.0'
    else:
        return 'j1.1'


def xsl_getter(sps_version):
    print("SPS version: %s" % sps_version)
    dtd_version = get_dtd_version(sps_version)
    return os.path.join(
        DTD_AND_XSL_PATH, XPM_FILES[dtd_version]["folder"],
        'xsl', 'sgml2xml', 'sgml2xml.xsl'
    )


def dtd_locations():
    locations = {}
    for version in XPM_FILES.sections():
        dtd_info = XPM_FILES[version]
        dtd_id = dtd_info['dtd_id']
        if dtd_id not in locations.keys():
            locations[dtd_id] = [
                dtd_info['remote'],
                dtd_info['remote'].replace('https:', 'http:')]
    return locations


def dtd_files(sps_version, database='scielo'):
    dtd_version = get_dtd_version(sps_version)
    return DTDFiles(database, dtd_version)


class DTDFiles(object):

    def __init__(self, database_name, version):
        self.database_name = database_name
        self.version = version
        if version in XPM_FILES:
            self.data = XPM_FILES[version]
        else:
            self.data = XPM_FILES[DEFAULT_VERSION]

    @property
    def real_dtd_path(self):
        return os.path.join(
            DTD_AND_XSL_PATH, self.data['dtd_path'], self.data['local'])

    @property
    def xsl_prep_report(self):
        return os.path.join(DTD_AND_XSL_PATH, self.data['xsl_prep_report'])

    @property
    def xsl_report(self):
        return os.path.join(DTD_AND_XSL_PATH, self.data['xsl_report'])

    @property
    def xsl_output(self):
        return os.path.join(
                DTD_AND_XSL_PATH,
                self.data['xsl_output_{}'.format(self.database_name)])
