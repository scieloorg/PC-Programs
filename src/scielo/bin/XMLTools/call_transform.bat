set JAVA_EXE=%1
set XML_TOOLS_PATH=%2
set xml_filename=%3
set xsl_filename=%4
set transformation_result_filename=%5
set error_filename=%6

if exist %transformation_result_filename%.tmp del %transformation_result_filename%.tmp
if exist %transformation_result_filename% del %transformation_result_filename%
if exist %error_filename% del %error_filename%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %transformation_result_filename%.tmp %xml_filename% %xsl_filename% 

if not exist %transformation_result_filename%.tmp echo Transformation error  > %error_filename%
if not exist %transformation_result_filename%.tmp echo %0 %1 %2 %3 %4 %5 %6 %7  >> %error_filename%

if exist %transformation_result_filename%.tmp copy %transformation_result_filename%.tmp %transformation_result_filename%

if exist %transformation_result_filename%.tmp del %transformation_result_filename%.tmp

