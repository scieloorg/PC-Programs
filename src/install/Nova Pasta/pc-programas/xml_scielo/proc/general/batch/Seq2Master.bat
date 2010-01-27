rem @echo off
rem Seq2Master.bat
rem Parametro 1: arquivo seq
rem Parametro 2: delimitador pipe ou space
rem Parametro 3: base a ser gerada
rem Parametro 4: proc [opcional]

call batch\VerifPresencaParametro.bat %0 @%1 arquivo seq
call batch\VerifExisteArquivo.bat %1
call batch\VerifPresencaParametro.bat %0 @%2 delimitador pipe space
call batch\VerifPresencaParametro.bat %0 @%3 base_de_dados a ser gerada

echo -all>temp\Seq2Master.in

if not "@%4"=="@" echo proc=@%4 >>temp\Seq2Master.in

call batch\InformaLog.bat %0 x Gera Master: %3
if "%2"=="space" goto SKIP_PIPE_SEQ
   %CISIS_DIR%\mx mfrl=30000 seq=%1 create=%3 now in=temp\Seq2Master.in
   if errorlevel==1 batch\AchouErro.bat %0 mx seq:%1 create:%3 [proc:@%4]
:SKIP_PIPE_SEQ

if "%2"=="pipe" goto SKIP_SPACE_SEQ
   %CISIS_DIR%\mx mfrl=30000 "seq=%1 " create=%3 now in=temp\Seq2Master.in
   if errorlevel==1 batch\AchouErro.bat %0 mx seq:%1 create:%3 [proc:@%4]
:SKIP_SPACE_SEQ
