set JAVA_EXE=%1
set XML_TOOLS_PATH=%2

set xml_filename=%3
rem validate_dtd opcional --validate USED IN CASE OF VALIDATE AGAINST DTD
set xsl_filename=%4
set transformation_result_filename=%5

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 %xml_filename% %xsl_filename% >  %transformation_result_filename%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 %xml_filename% %xsl_filename%