@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

set acron=%1
set issueid=%2
set filename=%3
set captura=%4
set ERROR_FILENAME=%5
set WARN_FILENAME=%6
set validate=%7


echo finished> temp\validation_result

%JAVA_EXE% -cp %XML_SCIELO_PROGRAM_PATH%\..\bin\jar\XMLCheck.jar br.bireme.XMLCheck.XMLCheck  %filename% %validate% > temp\validation_result

echo finished>>temp\validation_result


%MX% seq=temp\validation_result create=temp\validation_result now -all
%MX% temp\validation_result count=1 now

%MX% temp\validation_result count=1 lw=9999 "pft=if instr(v1,'finished')=0 then 'call scripts\handle_validation_result.bat %filename% %1 %2 %ERROR_FILENAME% %WARN_FILENAME% ',v1,' %captura%',# fi" now > temp\handle_validation_result.bat
%MX% temp\validation_result count=1 lw=9999 "pft=if instr(v1,'finished')>0 then '%acron% %issueid%'/ fi" now >> %OK_LIST%

call temp\handle_validation_result.bat


