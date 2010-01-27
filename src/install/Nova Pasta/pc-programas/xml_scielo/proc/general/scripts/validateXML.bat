@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

set acron=%1
set issueid=%2
set filename=%3
set validate=%5
set captura=%4


echo > temp\error
if exist temp\xml_error.txt del temp\xml_error.txt
%JAVA_EXE% -cp java\validador\XMLCheck.jar br.bireme.XMLCheck.XMLCheck  %filename% %validate% > temp\error


echo >>temp\error

%MX% seq=temp\error create=temp\error now -all


%MX% temp\error count=1 lw=9999 "pft=if instr(v1,'finished')=0 then 'call scripts\displayErrors.bat %filename% %1 %2 %captura%' fi,#" now > temp\messageValidation.bat
%MX% temp\error count=1 lw=9999 "pft=if instr(v1,'finished')>0 then '%acron% %issueid%'/ fi" now >> %OK_LIST%

call temp\messageValidation.bat


