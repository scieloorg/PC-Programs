set XML_TOOLS_PATH=%1
set this2that=%2
set ISSUE_PATH=%3
set XML_FILE=%4
set FILENAME=%5

SET WORK=%ISSUE_PATH%\pmc\pmc_work
SET PACK=%ISSUE_PATH%\pmc\pmc_package
SET PATH_PMC_IMG=%ISSUE_PATH%\pmc\pmc_img
SET PATH_IMG=%ISSUE_PATH%\img
SET WORK_ART=%WORK%\%FILENAME%

if not exist %PACK% mkdir %PACK%

set  temp_batch_partial=%WORK_ART%\rename_files.bat
set temp_batch_complete=%WORK%\rename_files.bat
set temp_batch_seq=%XML_TOOLS_PATH%\temp.seq


if exist %this2that% %XML_TOOLS_PATH%\..\cfg\mx seq=%this2that% lw=9999 "pft=if p(v1) then if p(v2) then 'call %XML_TOOLS_PATH%\rename_img.bat ',v1,' ',v2,' %PACK% %WORK_ART% %PATH_PMC_IMG% %PATH_IMG% %XML_TOOLS_PATH%'/ else 'call %XML_TOOLS_PATH%\rename_article.bat %FILENAME% ',v1,' %ISSUE_PATH% %XML_FILE% %PACK% %WORK_ART% %ISSUE_PATH%\pdf\',if instr('%FILENAME%','-')>0 then mid('%FILENAME%',1,instr('%FILENAME%','-')-1), else '%FILENAME%' fi '.pdf'/, fi fi" now > %temp_batch_partial%
if exist %temp_batch_partial% call %temp_batch_partial% 

if exist %temp_batch_seq% del %temp_batch_seq%

copy  %temp_batch_complete%  %temp_batch_seq%


%XML_TOOLS_PATH%\..\cfg\mx "seq=%temp_batch_seq%" lw=9999 "pft=if not v1:'call %temp_batch_partial%' then v1/ fi" now | sort >  %temp_batch_complete%

echo call %temp_batch_partial% >> %temp_batch_complete%
