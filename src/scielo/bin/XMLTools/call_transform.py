#set JAVA_EXE=%1
#set XML_TOOLS_PATH=%2
#set xml_filename=%3
#set xsl_filename=%4
#set transformation_result_filename=%5
#set error_filename=%6
#set ctrl_filename=%7

#if exist %ctrl_filename% del %ctrl_filename% 
#if exist %transformation_result_filename%.tmp del %transformation_result_filename%.tmp
#if exist %transformation_result_filename% del %transformation_result_filename%
#if exist %error_filename% del %error_filename%

#%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %transformation_result_filename%.tmp %xml_filename% %xsl_filename% 

#if not exist %transformation_result_filename%.tmp echo Transformation error  > %error_filename%
#if not exist %transformation_result_filename%.tmp echo %0 %1 %2 %3 %4 %5 %6 %7  >> %error_filename%
#if not exist %transformation_result_filename%.tmp echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %transformation_result_filename%.tmp %xml_filename% %xsl_filename% >> %error_filename%


#if exist %transformation_result_filename%.tmp copy %transformation_result_filename%.tmp %transformation_result_filename%

#if exist %transformation_result_filename%.tmp del %transformation_result_filename%.tmp

#echo fim > %ctrl_filename%

import os, sys, shutil, time

def check_file(filename, content='', taken_time=0, max_taken_time=100):
    c = ''
    start = time.time()
    r = False
    if os.path.exists(filename):
        try:
            f = open(filename, 'r')
            c = f.read()
            f.close()
             
            if len(c)>0:
                r = (len(content) == len(c))
            
        except:
            r = False

    end = time.time()
    print(taken_time)
    if r == False:
        taken_time += taken_time - start + end
        if taken_time < max_taken_time:
            r = check_file(filename, c, taken_time, max_taken_time)
    return r


def execute_command_line(command_line):
    import shlex, subprocess
    p = subprocess.Popen(shlex.split(command_line))
    p.wait()


script, java_exe, curr_path, xml_filename, xsl_filename, transformation_result_filename, error_filename, ctrl_filename = sys.argv
temp = transformation_result_filename + '.tmp'
files = [ctrl_filename, transformation_result_filename, temp, error_filename]
for f in files:
    if os.path.exists(f):
        os.unlink(f)

cmd = 'java -jar ' + curr_path  + '/core/saxon8.jar -novw -w0 -o ' + temp + ' ' + xml_filename + '  ' + xsl_filename 

os.system(cmd)
check_file(temp)

#execute_command_line(cmd)


if os.path.exists(temp):
    shutil.copyfile(temp, transformation_result_filename)
    os.unlink(temp)

f = open(ctrl_filename, 'w')
f.write('fim')
f.close()