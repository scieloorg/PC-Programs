# coding=utf-8
import os
import sys

from .app.config import app_texts
from .app.config import app_caller

THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
BIN_MARKUP_PATH = BIN_PATH + '/markup'
JAR_PATH = BIN_PATH + '/jar'
CONFIG_PATH = BIN_XML_PATH + '/config'
TABLES_PATH = BIN_XML_PATH + '/tables'
LOCALE_PATH = BIN_XML_PATH + '/locale'
TMP_DIR = BIN_PATH + '/tmp'
PMC_PATH = BIN_PATH + '/pmc'
HTML_REPORTS_PATH = BIN_XML_PATH + '/modules/generics/reports/'
FST_PATH = BIN_PATH + '/xml/modules'
VENV_PATH = BIN_PATH + '/xml/venv/scielo-programs'
REQUIREMENTS_PATH = BIN_PATH + '/xml/modules/venv/'.format(THIS_LOCATION)

_ = app_texts.get_texts(LOCALE_PATH)


appcaller = app_caller.AppCaller(VENV_PATH)
