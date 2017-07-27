# coding=utf-8
import os

from .app.config import app_texts


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

_ = app_texts.get_texts(LOCALE_PATH)
