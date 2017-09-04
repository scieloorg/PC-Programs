# coding=utf-8
import os

from .app.config import app_texts
from .app.config import app_caller


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
JAR_PATH = BIN_PATH + '/jar'
CONFIG_PATH = BIN_XML_PATH + '/app_config'
TABLES_PATH = BIN_XML_PATH + '/app_core/settings/tables'
LOCALE_PATH = BIN_XML_PATH + '/app_core/settings/locale'
TMP_DIR = BIN_PATH + '/tmp'
PMC_PATH = BIN_PATH + '/pmc'
HTML_REPORTS_PATH = BIN_XML_PATH + '/app_modules/generics/reports/'
FST_PATH = BIN_PATH + '/xml/app_modules'
VENV_PATH = BIN_PATH + '/xml/app_data/venv/scielo-programs'
REQUIREMENTS_FILE = BIN_PATH + '/xml/app_modules/settings/requirements.txt'
REQUIREMENTS_CHECKER = BIN_PATH + '/xml/app_modules/tools/requirements_checker.py'
EMAIL_TEMPLATE_MESSAGES_PATH = BIN_XML_PATH + '/app_core/settings/email'


_ = app_texts.get_texts(LOCALE_PATH)


appcaller = app_caller.AppCaller(VENV_PATH)
