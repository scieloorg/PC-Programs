# coding=utf-8
import os

from prodtools.config import app_texts


join_paths = os.path.join

PRODTOOLS_PATH = os.path.dirname(os.path.realpath(__file__))

BIN_PATH = os.path.dirname(os.path.dirname(PRODTOOLS_PATH))
BIN_XML_PATH = join_paths(BIN_PATH, "xml")
BIN_MARKUP_PATH = join_paths(BIN_PATH, 'markup')
XC_SERVER_CONFIG_PATH = join_paths(BIN_PATH, 'config')
TMP_DIR = join_paths(BIN_PATH, 'tmp')
LOG_PATH = join_paths(BIN_PATH, 'logs')
PMC_PATH = join_paths(BIN_PATH, 'pmc')

TABLES_PATH = join_paths(PRODTOOLS_PATH, 'settings', 'tables')
LOCALE_PATH = join_paths(PRODTOOLS_PATH, 'locale')
FST_PATH = join_paths(PRODTOOLS_PATH, 'settings', 'fst')
EMAIL_TEMPLATE_MESSAGES_PATH = join_paths(PRODTOOLS_PATH, 'settings', 'email')
HTML_REPORTS_PATH = join_paths(PRODTOOLS_PATH, 'reports')

if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)


_ = app_texts.get_texts(LOCALE_PATH)
