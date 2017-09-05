# coding=utf-8
import os

from .app.config import app_texts
from .app.config import app_caller


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
JAR_PATH = BIN_PATH + '/jar'
TMP_DIR = BIN_PATH + '/tmp'
PMC_PATH = BIN_PATH + '/pmc'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
CONFIG_PATH = BIN_XML_PATH + '/app_config'
VENV_PATH = BIN_XML_PATH + '/app_data/venv/scielo-programs'
TABLES_PATH = BIN_XML_PATH + '/app_modules/settings/tables'
LOCALE_PATH = BIN_XML_PATH + '/app_modules/settings/locale'
FST_PATH = BIN_XML_PATH + '/app_modules/settings/fst'
EMAIL_TEMPLATE_MESSAGES_PATH = BIN_XML_PATH + '/app_modules/settings/email'
REQUIREMENTS_FILE = BIN_XML_PATH + '/app_modules/settings/requirements.txt'
REQUIREMENTS_CHECKER = BIN_XML_PATH + '/app_modules/tools/requirements_checker.py'
HTML_REPORTS_PATH = BIN_XML_PATH + '/app_modules/generics/reports/'


_ = app_texts.get_texts(LOCALE_PATH)


appcaller = app_caller.AppCaller(VENV_PATH)
