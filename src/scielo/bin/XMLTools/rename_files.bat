set XML_TOOLS_PATH=%1
set this2that=%2
set ISSUE_PATH=%3
set XML_FILE=%4
set FILENAME=%5

SET WORK_ART=%ISSUE_PATH%\pmc_work\%FILENAME%
SET WORK=%ISSUE_PATH%\pmc_work

if not exist %ISSUE_PATH%\img mkdir %ISSUE_PATH%\img
if not exist %ISSUE_PATH%\pmc mkdir %ISSUE_PATH%\pmc
if not exist %WORK_ART%       mkdir %WORK_ART%
if not exist %WORK%           mkdir %WORK%

set  temp_batch_partial=%WORK_ART%\rename_files.bat
set temp_batch_complete=%WORK%\rename_files.bat
set temp_batch_seq=%XML_TOOLS_PATH%\temp.seq


if exist %this2that% %XML_TOOLS_PATH%\..\cfg\mx seq=%this2that% lw=9999 "pft=if p(v1) then if p(v2) then 'call %XML_TOOLS_PATH%\rename_img.bat ',v1,' ',v2,' %ISSUE_PATH%\pmc %WORK_ART% %ISSUE_PATH%\img_src  %ISSUE_PATH%\img '/ else 'call %XML_TOOLS_PATH%\rename_article.bat %FILENAME% ',v1,' %ISSUE_PATH% %XML_FILE% '/, fi fi" now > %temp_batch_partial%
if exist %temp_batch_partial% call %temp_batch_partial% 

if exist %temp_batch_seq% del %temp_batch_seq%

copy  %temp_batch_complete%  %temp_batch_seq%


%XML_TOOLS_PATH%\..\cfg\mx "seq=%temp_batch_seq%" lw=9999 "pft=if v1<>'call %temp_batch_partial%' then v1/ fi" now >  %temp_batch_complete%

echo call %temp_batch_partial% >> %temp_batch_complete%
