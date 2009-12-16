echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

echo %1 >> %XML_ERRORS%
echo %2 %3 >> %REPROCESS%

more temp\error >> %XML_ERRORS%
more temp\error >> %LOG%

if exist temp\xml_error.txt del temp\xml_error.txt

if "@%4"=="@CAPTURA_ERRO" echo ERROR > temp\xml_error.txt
if "@%4"=="@CAPTURA_ERRO" echo fim >> temp\xml_error.txt

