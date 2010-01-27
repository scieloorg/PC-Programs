rem VerifPresencaParametro
rem Parametro 1: batch
rem Parametro 2: parametro para verificar
rem Parametro 3..9: mensagem

if "%2"=="@" batch\AchouErro.bat %1 Falta parametro: %3 %4 %5 %6 %7 %8 %9
