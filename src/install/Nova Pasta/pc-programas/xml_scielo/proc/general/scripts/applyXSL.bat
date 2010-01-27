@echo off
set dest=%1
set xsl=%2
set xml_filename=%3
set acron=%4
set issueid=%5
set encoding=%6

more line.txt

echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

SET tempXML=temp\%dest%_%acron%%issueid%.xml
set tempFileName=temp\%xml_filename%

echo Generating temporary XML %tempXML% >> %LOG%
echo %WXIS% IsisScript=xis\xml_scielo_articles.xis path_db=%PATH_DB% pm_provider_id=%ID% mydb=%mydbinv% acron=%acron% issueid=%issueid% ahpdate=%ahpdate% encoding=%encoding%  cipar=%CIPAR_FILE% xml=%tempXML%  debug=%debug% >> %LOG%
%WXIS% IsisScript=xis\xml_scielo_articles.xis path_db=%PATH_DB% pm_provider_id=%ID% mydb=%mydbinv% acron=%acron% issueid=%issueid% ahpdate=%ahpdate% encoding=%encoding%  cipar=%CIPAR_FILE% xml=%tempXML%  debug=%debug% >> %LOG%

echo Validating temporary XML %tempXML% >> %LOG%
call scripts\validateXML.bat %4 %5 %tempXML% CAPTURA_ERRO
if exist temp\xml_error.txt goto ERROR1


echo Generating the XML wanted >> %LOG%
call scripts\transform.bat %tempXML% %xsl% %tempFileName%


echo Validating the XML wanted %tempFileName% >> %LOG%
call scripts\validateXML.bat %4 %5 %tempFileName% CAPTURA_ERRO --validate
if exist temp\xml_error.txt goto ERROR2

if not "@%7"=="@" call scripts\transform.bat %tempXML% %7 %tempFileName%

echo Transfering %tempFileName% >> %LOG%
call scripts\transfer.bat %dest% %acron% %issueid% %tempFileName% %xml_filename%


goto END

:ERROR1
echo  Errors found in general\%tempXML%. 
echo 
echo  To see the errors found
echo    Or open %xml_filename%.err 
echo    Or open %XML_SCIELO_PROGRAM_PATH%\proc\general\%tempXML% in a XML validation tool, for example, XML Spy.
echo
call scripts\transfer.bat %dest% %acron% %issueid% temp\error %xml_filename%.err


goto END

:ERROR2
echo  Errors found in general\%tempFileName%. 
echo 
echo  To see the errors found
echo    Or open %xml_filename%.err 
echo    Or open %XML_SCIELO_PROGRAM_PATH%\proc\general\%tempFileName% in a XML validation tool, for example, XML Spy.
echo
call scripts\transfer.bat %dest% %acron% %issueid% temp\error %xml_filename%.err

goto END

:END

more line.txt

