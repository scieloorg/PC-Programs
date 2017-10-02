# coding=utf-8
import os

try:
    from app_modules.app.config import app_texts
    from app_modules.app.config import app_caller
    from app_modules.generics import logger
except:
    from .app.config import app_texts
    from .app.config import app_caller
    from .generics import logger


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
JAR_PATH = BIN_PATH + '/jar'
TMP_DIR = BIN_PATH + '/tmp'
LOG_PATH = BIN_PATH + '/logs'
PMC_PATH = BIN_PATH + '/pmc'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
XC_SERVER_CONFIG_PATH = BIN_PATH + '/config'
VENV_PATH = BIN_XML_PATH + '/app_data/venv/scielo-programs'
TABLES_PATH = BIN_XML_PATH + '/app_modules/settings/tables'
LOCALE_PATH = BIN_XML_PATH + '/app_modules/settings/locale'
FST_PATH = BIN_XML_PATH + '/app_modules/settings/fst'
EMAIL_TEMPLATE_MESSAGES_PATH = BIN_XML_PATH + '/app_modules/settings/email'
REQUIREMENTS_FILE = BIN_XML_PATH + '/app_modules/settings/requirements.txt'
REQUIREMENTS_FILE_SPECIAL = BIN_XML_PATH + '/app_modules/settings/requirements-w64.txt'
REQUIREMENTS_CHECKER = BIN_XML_PATH + '/app_modules/tools/requirements_checker.py'
HTML_REPORTS_PATH = BIN_XML_PATH + '/app_modules/generics/reports/'


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
    VENV_PATH)
