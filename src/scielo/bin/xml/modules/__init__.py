# coding=utf-8
import os

from .config import app_texts


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
BIN_PATH = THIS_LOCATION + '/../..'
BIN_XML_PATH = BIN_PATH + '/xml'
JAR_PATH = BIN_PATH + '/jar'
CONFIG_PATH = BIN_XML_PATH + '/config'
TABLES_PATH = BIN_XML_PATH + '/tables'
LOCALE_PATH = BIN_XML_PATH + '/locale'
TMP_DIR = BIN_PATH + '/tmp'

_ = app_texts.get_texts(LOCALE_PATH)
