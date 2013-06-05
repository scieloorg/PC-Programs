echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

set filename=%1
set acron=%2
set issueid=%3
set ERROR_FILENAME=%4
set WARN_FILENAME=%5
set status=%6
set captura=%7




echo %filename% >> %XML_ERRORS%
echo %acron% %issueid% >> %REPROCESS%

more temp\validation_result >> %XML_ERRORS%
more temp\validation_result >> %LOG%


if not "@%captura%"=="@CAPTURA_ERRO" goto OVER

if "@%status%"=="@XXX" goto REPORT_WARNING


copy temp\validation_result %ERROR_FILENAME%
echo .
echo %filename% has errors.
echo Read %ERROR_FILENAME%
echo Try to validate %filename%, using any XML Validation Tool (Web browser, Oxygen, XML Spy, etc)
goto OVER

:REPORT_WARNING
echo WARNING > %WARN_FILENAME%
echo unable to validate >> %WARN_FILENAME%
echo .
echo UNABLE TO VALIDATE %filename%
echo Try to validate %filename%, using any XML Validation Tool (Web browser, Oxygen, XML Spy, etc)


:OVER



