# coding=utf-8
import os

from prodtools.config import app_texts


path_join = os.path.join

PRODTOOLS_PATH = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR_PARENT_PATH = os.path.dirname(os.getcwd())
CURRENT_NAME = os.path.basename(os.getcwd())
print(CURRENT_DIR_PARENT_PATH)
print(CURRENT_NAME)

BIN_PATH = CURRENT_DIR_PARENT_PATH
BIN_MARKUP_PATH = path_join(BIN_PATH, 'markup')

XC_SERVER_CONFIG_PATH = path_join(CURRENT_DIR_PARENT_PATH, 'config')
LOG_PATH = path_join(CURRENT_DIR_PARENT_PATH, 'logs')

if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)
if not os.path.isdir(BIN_MARKUP_PATH):
    os.makedirs(BIN_MARKUP_PATH)

TABLES_PATH = path_join(PRODTOOLS_PATH, 'settings', 'tables')
LOCALE_PATH = path_join(PRODTOOLS_PATH, 'locale')
FST_PATH = path_join(PRODTOOLS_PATH, 'settings', 'fst')
EMAIL_TEMPLATE_MESSAGES_PATH = path_join(PRODTOOLS_PATH, 'settings', 'email')
HTML_REPORTS_PATH = path_join(PRODTOOLS_PATH, 'reports')
DTD_AND_XSL_PATH = path_join(PRODTOOLS_PATH, 'settings', 'dtd_and_xsl')

XPM_VERSION_FILE_PATH = path_join(PRODTOOLS_PATH, 'xpm_version.txt')

ICON = path_join(PRODTOOLS_PATH, 'settings', 'Scielo.ico')

_ = app_texts.get_texts(LOCALE_PATH)
