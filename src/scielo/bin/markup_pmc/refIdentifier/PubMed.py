#@java -DLucene_Path=%LOCAL_PATH%/db -cp %LOCAL_PATH%;%LOCAL_PATH%/Marcador.jar;%LOCAL_PATH%/dom4j-1.6.1.jar;%LOCAL_PATH%/FOLLibrary.jar;%LOCAL_PATH%/Lucene.jar;%lucene%;%LOCAL_PATH%/zeus.jar RefBib.PubMedCentral -infile:%1 -outfile:%2

import sys, os, shutil, time
from datetime import datetime

def log(logfile, msg):
    f = open(logfile, 'a+')
    f.write(msg + '\n')
    f.close()

def check_file(logfile, filename, content='', taken_time=0, max_taken_time=100):
    log(logfile, 'check_file ' + str(taken_time))
    c = ''
    start = time.time()
    log(logfile, datetime.today().isoformat())
    log(logfile, 'start: ' + str(start))
    r = False
    if os.path.exists(filename):
        try:
            f = open(filename, 'r')
            c = f.read()
            f.close()
            try:
                log(logfile, '' + c)
    
            except:
                log(logfile, 'cannot read the content')
            r = '</ref-list>'  in c
            
        except:
            r = False

    end = time.time()
    log(logfile, 'end: ' + str(end))
    log(logfile, datetime.today().isoformat())
    
    log(logfile, 'taken time: ' + str(end - start) )
    if r == False:
        taken_time +=  end - start 
        log(logfile, 'total taken time: ' + str(taken_time) )
        if taken_time < max_taken_time:
            r = check_file(logfile, filename, c, taken_time, max_taken_time)
    return r


fixed = [ item.replace('\\', '/') for item in sys.argv ]
script, mkpfilename, result_filename, ctrl_filename, local_path, standard = fixed

lucene = local_path + '/lucene-core-2.3.2.jar'

temp_file = ctrl_filename + '.tmp'
if os.path.exists(temp_file):
    os.unlink(temp_file)

logfilename = ctrl_filename + '.log'
if os.path.exists(logfilename):
    os.unlink(logfilename)
if os.path.exists(ctrl_filename):
    os.unlink(ctrl_filename)
if os.path.exists(result_filename):
    os.unlink(result_filename)

cmd = '@java -DLucene_Path=' + local_path + '/db -cp ' + local_path + ';' + local_path + '/Marcador.jar;' + local_path + '/dom4j-1.6.1.jar;' + local_path + '/FOLLibrary.jar;'+ local_path + '/Lucene.jar;' + lucene + ';'+ local_path + '/zeus.jar RefBib.PubMedCentral -infile:' + mkpfilename + ' -outfile:' + temp_file 

os.system(cmd)

check_file(logfilename, temp_file, '', 0, 100)

shutil.copyfile(temp_file, result_filename)
shutil.copyfile(temp_file, ctrl_filename)
