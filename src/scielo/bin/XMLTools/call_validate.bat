set JAVA_EXE=%1
set XML_TOOLS_PATH=%2
set xml_filename=%3
rem validate_dtd opcional --validate USED IN CASE OF VALIDATE AGAINST DTD
set validate_dtd=%4
set validation_result_filename=%5

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %xml_filename% %validate_dtd% > %validation_result_filename%
