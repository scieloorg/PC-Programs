@echo off
set dest=%1
set xsl=%2
set xml_filename=%3
set acron=%4
set issueid=%5
set encoding=%6
set ahpdate=%7
set maxdate=%8

set ERROR_FILENAME=temp\xml_erros.txt
set WARN_FILENAME=temp\xml_warnings.txt

more line.txt

echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

SET GENERIC_XML_FILENAME=temp\%dest%_%acron%%issueid%.xml
set TEMP_SPEC_XML_FILENAME=temp\%xml_filename%

echo Generating generic XML  %GENERIC_XML_FILENAME% >> %LOG%
echo %WXIS% IsisScript=xis\xml_scielo_articles.xis path_db=%PATH_DB% pm_provider_id=%ID% mydb=%mydbinv% acron=%acron% issueid=%issueid% ahpdate=%ahpdate% maxdate=%maxdate% encoding=%encoding%  cipar=%CIPAR_FILE% xml=%GENERIC_XML_FILENAME%  debug=%debug% >> %LOG%
%WXIS% IsisScript=xis\xml_scielo_articles.xis path_db=%PATH_DB% pm_provider_id=%ID% mydb=%mydbinv% acron=%acron% issueid=%issueid% ahpdate=%ahpdate% maxdate=%maxdate%  encoding=%encoding%  cipar=%CIPAR_FILE% xml=%GENERIC_XML_FILENAME%  debug=%debug% >> %LOG%

if exist scripts/fix.py python scripts/fix.py %PATH_DB%/%acron%/%issueid%/base

echo Validating generic XML  %GENERIC_XML_FILENAME% >> %LOG%
call scripts\validateXML.bat %4 %5 %GENERIC_XML_FILENAME% CAPTURA_ERRO %ERROR_FILENAME% %WARN_FILENAME%
rem if exist %ERROR_FILENAME% goto END



echo Generating the  expected XML  >> %LOG%
call scripts\transform.bat %GENERIC_XML_FILENAME% %xsl% %TEMP_SPEC_XML_FILENAME%


echo Validating the  expected XML  %TEMP_SPEC_XML_FILENAME% >> %LOG%
call scripts\validateXML.bat %4 %5 %TEMP_SPEC_XML_FILENAME% CAPTURA_ERRO %ERROR_FILENAME% %WARN_FILENAME% --validate
rem if exist %ERROR_FILENAME% goto END

if %xsl% == "xsl\ISI_validator.xsl" call scripts\transform.bat %GENERIC_XML_FILENAME% xs\ISI.xsl %TEMP_SPEC_XML_FILENAME%

echo Transfering %TEMP_SPEC_XML_FILENAME% >> %LOG%
if exist %TEMP_SPEC_XML_FILENAME% call scripts\transfer.bat %dest% %acron% %issueid% %TEMP_SPEC_XML_FILENAME% %xml_filename%



:END
if exist %ERROR_FILENAME% copy %ERROR_FILENAME% %PATH_DB%\%acron%\%issueid%\%dest%\%xml_filename%.err
more line.txt

