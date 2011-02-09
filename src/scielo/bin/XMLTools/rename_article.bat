REM %FILENAME% %ISSUE_PATH% %XML_FILE% ',v1

set FILENAME=%1
set ISSUE_PATH=%2
set XML_FILE=%3
set NEW_FILENAME=%4

rem RENOMEIA IMAGEM ORIGINAL TIFF PARA PMC

if exist %XML_FILE%                      copy %XML_FILE%                       %ISSUE_PATH%\pmc\%NEW_FILENAME%.xml
if exist %XML_FILE%                      copy %XML_FILE%                       %ISSUE_PATH%\pmc_temp\%NEW_FILENAME%_ALIAS_%FILENAME%.xml

if exist %ISSUE_PATH%\pdf\%FILENAME%.pdf copy %ISSUE_PATH%\pdf\%FILENAME%.pdf  %ISSUE_PATH%\pmc\%NEW_FILENAME%.pdf
