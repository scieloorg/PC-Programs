@echo off


rem Inicializa variaveis
set SHELL=C:\COMMAND.COM /P /E:1024
set CISIS_DIR=..\cisis


rem Set parametros para execucao

set DATABASE_DESTINATION=%1
set LOG=log\GeraXML.log

set INFORMALOG=%LOG%
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%


call batch\ReadConfigFile.bat ..\..\..\bin\scielo_paths.ini %CISIS_DIR%\mx
call batch\ReadConfigFile.bat ..\..\config\xml_scielo.ini %CISIS_DIR%\mx

set XML_ERRORS=log\xml_errors.log

set CONFIG=%XML_SCIELO_PROGRAM_PATH%\config\PubMed\config\config
set JOURNALS=%XML_SCIELO_PROGRAM_PATH%\config\PubMed\journals\journals
set PATH_DB=%Serial_Directory%
set PROGRAM_PATH=%XML_SCIELO_PROGRAM_PATH%

echo setting php or java >> %LOG%
:SETPHP
if "@%PHP_EXE%"=="@" goto SETJAVA
echo trying to set php >> %LOG%
if exist %PHP_EXE% set PHP_TRANSFORMATION="%PHP_EXE% -f general\php\xml_xsl.php"
echo testing PHP_TRANSFORMATION=%PHP_TRANSFORMATION% >> %LOG%
if not exist %PHP_EXE% echo NOT FOUND php %PHP_EXE%>> %LOG%

:SETJAVA
if "@%JAVA_EXE%"=="@" goto SETTRANFORMER
echo trying to set java >> %LOG%
if exist %JAVA_EXE% set JAVA_TRANSFORMATION="%JAVA_EXE%"

echo testing JAVA_TRANSFORMATION=%JAVA_EXE% >> %LOG%
if not exist %JAVA_EXE% echo NOT FOUND java %JAVA_EXE%>> %LOG%

if "@%PHP_EXE%@%JAVA_EXE%@"=="@@@" goto ERROR

:SETTRANFORMER

set ID=%PUBMED_PROVIDER_ID%
set FST=fst\xml_scielo.fst
set SCI_LISTA=%XML_SCIELO_PROGRAM_PATH%\scilista_%1.lst
SET REPROCESS=%XML_SCIELO_PROGRAM_PATH%\scilista_%1_errxml.lst
set REPROCESSFALTADB=%XML_SCIELO_PROGRAM_PATH%\scilista_%1_faltabd.lst
SET OK_LIST=%XML_SCIELO_PROGRAM_PATH%\scilista_%1_ok.lst

rem bases de dados
set FORMER_TITLE=%Serial_Directory%title\title
set TITLE=temp\title
SET CIPAR_FILE=..\..\config\arquivo.cip

more empty.txt > %OK_LIST%
more empty.txt > %REPROCESS%
more empty.txt > %REPROCESSFALTADB%

more empty.txt > %XML_ERRORS%
more empty.txt > %LOG%
md temp  >> %LOG%

if not exist %SCI_LISTA% copy %SCI_LISTA_SITE% %SCI_LISTA%


rem Apresentar o conteúdo de scilista.lst para confirmar
echo === ATENCAO ===
echo Este arquivo executara a geração de xml para %DATABASE_DESTINATION% das seguintes revistas
echo.
echo Tecle CONTROL-C para sair ou ENTER para verificar as revistas...

pause > nul

call notepad "%SCI_LISTA%"

cls
echo === ATENCAO ===
echo.
echo Serao gerados os xml para serem enviados a %DATABASE_DESTINATION%
echo.
echo Tecle CONTROL-C para sair ou ENTER para continuar...

pause > nul

echo Apagatemp
call batch\Apagatemp.bat

echo Preparing data
call batch\Seq2Master.bat %CONFIG%.seq space %CONFIG%
call batch\GeraInvertido.bat %CONFIG% %CONFIG%.fst %CONFIG%
call batch\Seq2Master.bat %JOURNALS%.seq space %JOURNALS%
call batch\GeraInvertido.bat %JOURNALS% %JOURNALS%.fst %JOURNALS%

copy %FORMER_TITLE%.* temp  >> %LOG%
call batch\GeraInvertido.bat %TITLE% fst\title.fst %TITLE%

echo Generating XML



%MX% "seq=%SCI_LISTA% " lw=9999 "pft=if p(v1) then 'call scripts\generateXML.bat %MX% %DATABASE_DESTINATION% ',v1,' ',v2,' ',v3,' ',v4,' ',v5/ fi" now> temp\generateXML4scilista.bat
call temp\generateXML4scilista.bat

if not "%1"=="PUBMED" goto END
if not exist ..\..\..\bin\xml\prodtools\xml_pubmed.py goto END
%MX% "seq=%SCI_LISTA% " lw=9999 "pft=if p(v1) then 'cd ..\..\..\bin\xml'/,'scielo2pubmed %Serial_Directory%\',v1,'\',v2,' ',v4,' ',v5/ fi" now> temp\xml_pubmed.bat
call temp\xml_pubmed.bat
goto END

:ERROR
echo Missing PHP_EXE or JAVA_EXE

:END
if exist %REPROCESS% echo %REPROCESS% issues to reprocess
if exist %REPROCESSFALTADB% echo %REPROCESSFALTADB% issues which db is missing 
if exist %OK_LIST% echo %OK_LIST% issues OK 


REM echo End of %0 %1 %2 %3 %4 

cd ..\..\xml_scielo\proc

