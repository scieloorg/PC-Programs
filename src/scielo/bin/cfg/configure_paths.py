# coding=utf-8
import os
import sys
import shutil

APPDIR = sys.argv[1]
DATADIR = sys.argv[2] if len(sys.argv) > 2 else None
MYSCIELOURL = sys.argv[3] if len(sys.argv) > 2 else None
WEBPATH = sys.argv[4] if len(sys.argv) > 2 else None

scielo_cfg_filename = os.path.join(APPDIR, 'bin', 'scielo_paths.ini')
bkp_scielo_cfg_filename = os.path.join(APPDIR, 'bin', 'scielo_paths.ini.old')
template_scielo_cfg_filename = os.path.join(APPDIR, 'bin', 'scielo_paths.example.ini')
template_parser_settings_filename = os.path.join(APPDIR, 'bin', 'cfg', 'Settings.cfg.template')
parser_settings_filename = os.path.join(APPDIR, 'bin', 'SGMLPars', Settings.cfg')


if os.path.exists(scielo_cfg_filename):    
    shutil.copyfile(scielo_cfg_filename, bkp_scielo_cfg_filename)    

f = open(template_scielo_cfg_filename, 'r')    
c = f.read()    
f.close()

f = open(scielo_cfg_filename, 'w')    
f.write(c.replace('d:\dados\scielo', sys.argv[2]).replace('c:\programas\scielo', sys.argv[1]).replace('MYSCIELOURL', sys.argv[3]))    
f.close()

f = open(template_parser_settings_filename, 'r')    
c = f.read()    
f.close()

f = open(sys.argv[1] + '/bin/SGMLPars/Settings.cfg', 'w')    
f.write(c.replace('C:\SCIELO', sys.argv[1]))
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
