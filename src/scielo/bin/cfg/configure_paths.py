# coding=utf-8
import os
import sys
import shutil


APPDIR = sys.argv[1]
DATADIR = sys.argv[2] if len(sys.argv) > 2 else None
MYSCIELOURL = sys.argv[3] if len(sys.argv) > 2 else None
WEBPATH = sys.argv[4] if len(sys.argv) > 2 else None

SCIELO_PATHS_CONFIG = os.path.join(APPDIR, 'bin', 'scielo_paths.ini')
SCIELO_PATHS_BKP = os.path.join(APPDIR, 'bin', 'scielo_paths.ini.old')
SCIELO_PATHS_TEMPLATE = os.path.join(APPDIR, 'bin', 'scielo_paths.example.ini')
PARSER_CONFIG_TEMPLATE = os.path.join(APPDIR, 'bin', 'cfg', 'Settings.cfg.template')
PARSER_CONFIG = os.path.join(APPDIR, 'bin', 'SGMLPars', 'Settings.cfg')


def update_parser_config():
    with open(PARSER_CONFIG_TEMPLATE, 'w') as fp:
        c = fp.read()
    with open(PARSER_CONFIG, 'w') as fp:
        f.write(c.replace('C:\\SCIELO', APPDIR))


if os.path.exists(SCIELO_PATHS_CONFIG):    
    shutil.copyfile(SCIELO_PATHS_CONFIG, SCIELO_PATHS_BKP)    

f = open(SCIELO_PATHS_TEMPLATE, 'r')    
c = f.read()    
f.close()

f = open(SCIELO_PATHS_CONFIG, 'w')    
f.write(c.replace('d:\dados\scielo', sys.argv[2]).replace('c:\programas\scielo', sys.argv[1]).replace('MYSCIELOURL', sys.argv[3]))    
f.close()


if os.path.exists(sys.argv[2] + '/serial/issue/issue.mst'):    
    os.system(sys.argv[1] + '/bin/cfg/mx ' + sys.argv[2] + '/serial/issue/issue fst=@ fullinv=' + sys.argv[2] + '/serial/issue/issue')

if not os.path.exists(sys.argv[2] + '/serial/code/newcode.fst'):    
    shutil.copyfile(sys.argv[2] + '/serial/code/code.fst', sys.argv[2] + '/serial/code/newcode.fst')    

if not os.path.exists(sys.argv[2] + '/serial/code/newcode.mst'):
    shutil.copyfile(sys.argv[2] + '/serial/code/code.mst', sys.argv[2] + '/serial/code/newcode.mst')
    shutil.copyfile(sys.argv[2] + '/serial/code/code.xrf', sys.argv[2] + '/serial/code/newcode.xrf')

os.system(sys.argv[1] + '/bin/cfg/mx ' + sys.argv[2] + '/serial/code/code fst=@ fullinv=' + sys.argv[2] + '/serial/code/code')    
os.system(sys.argv[1] + '/bin/cfg/mx ' + sys.argv[2] + '/serial/code/newcode fst=@ fullinv=' + sys.argv[2] + '/serial/code/newcode')

os.system('SET BAP=OS23470a')
