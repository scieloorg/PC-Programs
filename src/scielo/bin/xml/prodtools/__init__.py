# coding=utf-8
import os

from prodtools.config import app_texts


path_join = os.path.join

PRODTOOLS_PATH = os.path.dirname(os.path.realpath(__file__))

TWO_PARENTS_UPPER = os.path.dirname(os.path.dirname(PRODTOOLS_PATH))

BIN_PATH = ''
SERVER_WORKSPACE_PATH = ''
if os.path.basename(TWO_PARENTS_UPPER) == "bin":
    BIN_PATH = TWO_PARENTS_UPPER
    BIN_MARKUP_PATH = path_join(BIN_PATH, 'markup')
else:
    SERVER_WORKSPACE_PATH = os.getcwd()
    XC_SERVER_CONFIG_PATH = path_join(SERVER_WORKSPACE_PATH, 'config')
    LOG_PATH = path_join(SERVER_WORKSPACE_PATH, 'logs')
    BIN_MARKUP_PATH = path_join(SERVER_WORKSPACE_PATH, 'markup')
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



_ = app_texts.get_texts(LOCALE_PATH)
