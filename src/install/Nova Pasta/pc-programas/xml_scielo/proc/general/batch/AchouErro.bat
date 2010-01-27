rem AchouErro
rem Parametro 1: nome do batch
rem Parametro 2..9: mensagem

call batch\InformaLog.bat %1 dh ===ERRO===: %2 %3 %4 %5 %6 %7 %8
echo.
echo == ERRO ==============================================
echo Batch: %1
echo ------ %2 %3 %4 %5 %6 %7 %8 %9
echo =====================================================X
echo.
echo O log do processamento esta armazenado em: %INFORMALOG%
echo Tecle CONTROL-C para sair ou ENTER para continuar ...
pause >nul
