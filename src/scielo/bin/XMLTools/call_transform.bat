set JAVA_EXE=%1
set XML_TOOLS_PATH=%2
set xml_filename=%3
set xsl_filename=%4
set transformation_result_filename=%5

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 %xml_filename% %xsl_filename% >  %transformation_result_filename%.tmp

if not exist %transformation_result_filename%.tmp echo error > %transformation_result_filename% 
if exist %transformation_result_filename%.tmp copy %transformation_result_filename%.tmp %transformation_result_filename%
if exist %transformation_result_filename%.tmp del %transformation_result_filename%.tmp


