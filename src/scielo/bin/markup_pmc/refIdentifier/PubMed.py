#@REM argumento1 nome do arquivo com as marcacoes
#@REM argumento2 nome do arquivo de saida

#set LOCAL_PATH=%4
#echo mkpfilename %1
#echo parametro2 %2
#set lucene=%LOCAL_PATH%/lucene-core-2.3.2.jar

#del %3
#@java -DLucene_Path=%LOCAL_PATH%/db -cp %LOCAL_PATH%;%LOCAL_PATH%/Marcador.jar;%LOCAL_PATH%/dom4j-1.6.1.jar;%LOCAL_PATH%/FOLLibrary.jar;%LOCAL_PATH%/Lucene.jar;%lucene%;%LOCAL_PATH%/zeus.jar RefBib.PubMedCentral -infile:%1 -outfile:%2
#copy %2 %3
#@java -DLucene_Path=%LOCAL_PATH%/db -cp %LOCAL_PATH%;%LOCAL_PATH%/Marcador.jar;%LOCAL_PATH%/dom4j-1.6.1.jar;%LOCAL_PATH%/FOLLibrary.jar;%LOCAL_PATH%/Lucene.jar;%lucene%;%LOCAL_PATH%/zeus.jar RefBib.PubMedCentral -infile:%1 -outfile:%2

import sys, os, shutil

print(sys.argv)

def check_file(filename):
    r = False
    if os.path.exists(filename):
        r = True
    else:
        r = check_file(filename)
    return r

fixed = [ item.replace('\\', '/') for item in sys.argv ]
script, mkpfilename, result_filename, ctrl_filename, local_path, standard = fixed

lucene = local_path + '/lucene-core-2.3.2.jar'

if os.path.exists(ctrl_filename):
    os.unlink(ctrl_filename)
cmd = '@java -DLucene_Path=' + local_path + '/db -cp ' + local_path + ';' + local_path + '/Marcador.jar;' + local_path + '/dom4j-1.6.1.jar;' + local_path + '/FOLLibrary.jar;'+ local_path + '/Lucene.jar;' + lucene + ';'+ local_path + '/zeus.jar RefBib.PubMedCentral -infile:' + mkpfilename + ' -outfile:' + result_filename + '\n'
#cmd += 'copy ' + result_filename + ' ' + ctrl_filename
os.system(cmd)

print(os.path.exists(result_filename))


check_file(result_filename)
shutil.copyfile(result_filename, ctrl_filename)

print(os.path.exists(ctrl_filename))