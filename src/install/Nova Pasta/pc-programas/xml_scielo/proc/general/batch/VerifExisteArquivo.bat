rem VerifExisteArquivo
rem Parametro 1: arquivo

call batch\VerifPresencaParametro.bat %0 @%1 arquivo para ver se existe

call batch\InformaLog.bat %0 x Verifica se existe arquivo: %1
if not exist %1 batch\AchouErro.bat %0 Arquivo nao encontrado: %1