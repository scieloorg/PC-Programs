rem GeraInvertido
rem Parametro 1: base de dados
rem Parametro 2: fst 
rem Parametro 3: nome do invertido [opcional]

call batch\VerifPresencaParametro.bat %0 @%1 base de dados
call batch\VerifExisteBase.bat %1
call batch\VerifPresencaParametro.bat %0 @%2 fst
set INVBASE=%3
if "@%3"=="@" set INVBASE=%1

call batch\InformaLog.bat %0 x Gera invertido: %INVBASE%

echo READ.*=%1.*> temp\GeraInvertido.cip
%CISIS_DIR%\mx cipar=temp\GeraInvertido.cip READ gizmo=gizmo\Accent fst=@%2 fullinv/ansi=%INVBASE% now -all
if errorlevel==1 batch\AchouErro.bat %0 mx %1 fst:@%2 fullinv:%INVBASE%
