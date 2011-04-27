REM %FILENAME% %ISSUE_PATH% %XML_FILE% ',v1

set FILENAME=%1
set NEW_FILENAME=%2
set ISSUE_PATH=%3
set XML_FILE=%4

rem RENOMEIA arquivo xml 

if not exist %XML_FILE% goto END

copy %XML_FILE% %ISSUE_PATH%\pmc_work\%FILENAME%\%NEW_FILENAME%.xml
del %XML_FILE%

:END

if exist %ISSUE_PATH%\pmc_work\%FILENAME%\%NEW_FILENAME%.xml copy %ISSUE_PATH%\pmc_work\%FILENAME%\%NEW_FILENAME%.xml %ISSUE_PATH%\pmc\%NEW_FILENAME%.xml
if exist %ISSUE_PATH%\pdf\%FILENAME%.pdf copy %ISSUE_PATH%\pdf\%FILENAME%.pdf %ISSUE_PATH%\pmc\%NEW_FILENAME%.pdf

