set XML_TOOLS_PATH=%1
set this2that=%2
set ISSUE_PATH=%3
set XML_FILE=%4
set FILENAME=%5

set temp_batch=%XML_TOOLS_PATH%\temp.bat


if not exist %ISSUE_PATH%\img mkdir %ISSUE_PATH%\img
if not exist %ISSUE_PATH%\pmc mkdir %ISSUE_PATH%\pmc
if not exist %ISSUE_PATH%\pmc_temp mkdir %ISSUE_PATH%\pmc_temp


if exist %this2that% %XML_TOOLS_PATH%\..\cfg\mx seq=%this2that% lw=9999 "pft=if p(v1) then if p(v2) then 'call %XML_TOOLS_PATH%\rename_img.bat ',v1,' ',v2,' %ISSUE_PATH%\img_src  %ISSUE_PATH%\img  %ISSUE_PATH%\pmc  %ISSUE_PATH%\pmc_temp '/ else 'call %XML_TOOLS_PATH%\rename_article.bat %FILENAME% %ISSUE_PATH% %XML_FILE% ',v1/, fi fi" now > %temp_batch%
if exist %temp_batch% call %temp_batch% 




