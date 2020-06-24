# coding=utf-8
import os
import sys
import shutil
from datetime import datetime


def now():
    return datetime.now().isoformat().replace(
        " ", "-").replace(".", "-").replace(":", "-")

PYTHON3 = sys.argv[1]
APPDIR = sys.argv[2]
DATADIR = sys.argv[3] if len(sys.argv) > 2 else None
MYSCIELOURL = sys.argv[4] if len(sys.argv) > 2 else None
WEBPATH = sys.argv[5] if len(sys.argv) > 2 else None

SCIELO_PATHS_CONFIG = os.path.join(APPDIR, 'bin', 'scielo_paths.ini')
SCIELO_PATHS_TEMPLATE = os.path.join(APPDIR, 'bin', 'scielo_paths.example.ini')
PARSER_CONFIG_TEMPLATE = os.path.join(
    APPDIR, 'bin', 'cfg', 'Settings.cfg.template')
PARSER_CONFIG = os.path.join(APPDIR, 'bin', 'SGMLPars', 'Settings.cfg')
mainGenerateXMLfilename = os.path.join(
    APPDIR, 'xml_scielo', 'proc', 'general', 'mainGenerateXMLfilename.bat')


def fix_python_path_in_mainGenerateXML():
    with open(mainGenerateXMLfilename, 'r') as fp:
        c = fp.read()
    with open(mainGenerateXMLfilename, 'w') as fp:
        c = c.replace(
            ",'python xml_pubmed.py ",
            ",'{}\\python xml_pubmed.py ".format(PYTHON3))
        fp.write(c)


def update_parser_config():
    with open(PARSER_CONFIG_TEMPLATE, 'r') as fp:
        c = fp.read()
    with open(PARSER_CONFIG, 'w') as fp:
        c = c.replace('C:\\SCIELO', APPDIR)
        fp.write(c)


def update_scielo_paths():
    items = [
        ('d:\\dados\\scielo', DATADIR),
        ('c:\\programas\\scielo', APPDIR),
        ('MYSCIELOURL', MYSCIELOURL),
        ('SCI_LISTA_SITE=c:\\var\\www\\scielo',
            'SCI_LISTA_SITE={}'.format(WEBPATH)),
    ]

    if os.path.exists(SCIELO_PATHS_CONFIG):
        SCIELO_PATHS_BKP = SCIELO_PATHS_CONFIG + "." + now() + ".old"
        shutil.copyfile(SCIELO_PATHS_CONFIG, SCIELO_PATHS_BKP)

    with open(SCIELO_PATHS_TEMPLATE, 'r') as fp:
        c = fp.read()
    with open(SCIELO_PATHS_CONFIG, 'w') as fp:
        for old, new in items:
            if new:
                c = c.replace(old, new)
        fp.write(c)


def create_newcode_db():
    NEW_CODE_DB = os.path.join(DATADIR, "serial", "code", "newcode")
    CODE_DB = os.path.join(DATADIR, "serial", "code", "code")
    mx = os.path.join(APPDIR, "bin", "cfg", "mx")

    for ext in (".fst", ".mst", ".xrf"):
        if not os.path.exists(NEW_CODE_DB + ext):
            shutil.copyfile(CODE_DB + ext, NEW_CODE_DB + ext)

    for db in (CODE_DB, NEW_CODE_DB):
        cmd = "{} {} fst=@ fullinv={}".format(mx, db, db)
        os.system(cmd)


if __name__ == "__main__":
    update_parser_config()
    update_scielo_paths()
    create_newcode_db()
    fix_python_path_in_mainGenerateXML()

