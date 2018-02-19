# coding=utf-8
import os

try:
    from app_modules.app.config import app_texts
    from app_modules.app.config import app_caller
    from app_modules.generics import logger
    from app_modules.generics import encoding
except:
    from .app.config import app_texts
    from .app.config import app_caller
    from .generics import logger
    from .generics import encoding


THIS_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
THIS_LOCATION = encoding.decode(THIS_FILE_LOCATION, encoding.SYS_DEFAULT_ENCODING)

BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
JAR_PATH = BIN_PATH + '/jar'
JAR_PATH = JAR_PATH.replace(BIN_PATH, './..')
TMP_DIR = BIN_PATH + '/tmp'
LOG_PATH = BIN_PATH + '/logs'
PMC_PATH = BIN_PATH + '/pmc'
RELATIVE_PMC_PATH = './../pmc'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
XC_SERVER_CONFIG_PATH = BIN_PATH + '/config'
TABLES_PATH = BIN_XML_PATH + '/app_modules/settings/tables'
LOCALE_PATH = BIN_XML_PATH + '/app_modules/settings/locale'
FST_PATH = BIN_XML_PATH + '/app_modules/settings/fst'
EMAIL_TEMPLATE_MESSAGES_PATH = BIN_XML_PATH + '/app_modules/settings/email'
REQUIREMENTS_FILE = BIN_XML_PATH + '/app_modules/settings/requirements.txt'
REQUIREMENTS_CHECKER = BIN_XML_PATH + '/app_modules/tools/requirements_checker.py'
HTML_REPORTS_PATH = BIN_XML_PATH + '/app_modules/generics/reports/'


VENV_PATH = BIN_XML_PATH + '/app_data/venv/scielo-programs'
try:
    if not str(THIS_LOCATION) == THIS_FILE_LOCATION:
        VENV_PATH = '/scielo-virtualenv/venv'
except:
    VENV_PATH = '/scielo-virtualenv/venv'


if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)


_ = app_texts.get_texts(LOCALE_PATH)

try:
    os.unlink(LOG_PATH+'/app_caller.log')
except:
    pass


appcaller = app_caller.AppCaller(
    logger.get_logger(LOG_PATH+'/app_caller.log', 'Environment'),
    VENV_PATH,
    REQUIREMENTS_FILE)
