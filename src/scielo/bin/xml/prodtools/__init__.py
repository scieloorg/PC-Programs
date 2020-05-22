# coding=utf-8
import os

from prodtools.config import app_texts
from prodtools.utils import encoding


THIS_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
THIS_LOCATION = encoding.decode(THIS_FILE_LOCATION, encoding.SYS_DEFAULT_ENCODING)

INVALID_APP_PATH = not str(THIS_LOCATION) == THIS_FILE_LOCATION

BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
JAR_PATH = BIN_PATH + '/jar'
RELATIVE_JAR_PATH = JAR_PATH.replace(BIN_PATH, './..')
TMP_DIR = BIN_PATH + '/tmp'
LOG_PATH = BIN_PATH + '/logs'
PMC_PATH = BIN_PATH + '/pmc'
RELATIVE_PMC_PATH = './../pmc'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
XC_SERVER_CONFIG_PATH = BIN_PATH + '/config'
TABLES_PATH = BIN_XML_PATH + '/prodtools/settings/tables'
LOCALE_PATH = BIN_XML_PATH + '/prodtools/locale'
FST_PATH = BIN_XML_PATH + '/prodtools/settings/fst'
EMAIL_TEMPLATE_MESSAGES_PATH = BIN_XML_PATH + '/prodtools/settings/email'
REQUIREMENTS_FILE = BIN_XML_PATH + 'prodtools/settings/requirements.txt'
HTML_REPORTS_PATH = BIN_XML_PATH + '/prodtools/reports/'

if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)


_ = app_texts.get_texts(LOCALE_PATH)
