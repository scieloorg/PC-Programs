set ctrl_filename=%1
set JAVA_EXE=%2
set XML_TOOLS_PATH=%3
set xml_filename=%4
set validation_result_filename=%5
set validate_dtd=%6

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %xml_filename% %validate_dtd% > %validation_result_filename%.tmp

if exist %ctrl_filename% del %ctrl_filename% 

if not exist %validation_result_filename%.tmp echo error > %validation_result_filename%
if exist %validation_result_filename%.tmp copy %validation_result_filename%.tmp %validation_result_filename%
if exist %validation_result_filename%.tmp del %validation_result_filename%.tmp 

echo fim > %ctrl_filename%