set JAVA_EXE=%1
set XML_TOOLS_PATH=%2
set xml_filename=%3
set validation_result_filename=%4
set validate_dtd=%5

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %xml_filename% %validate_dtd% > %validation_result_filename%.tmp

if not exist %validation_result_filename%.tmp echo error > %validation_result_filename%
if exist %validation_result_filename%.tmp copy %validation_result_filename%.tmp %validation_result_filename%
if exist %validation_result_filename%.tmp del %validation_result_filename%.tmp
