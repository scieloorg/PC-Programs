rem VerifExisteBase
rem Parametro 1: base de dados

call batch\VerifPresencaParametro.bat %0 @%1 base de dados

call batch\InformaLog.bat %0 x Verifica se existe a base: %1
call batch\VerifExisteArquivo.bat %1.mst
call batch\VerifExisteArquivo.bat %1.xrf
