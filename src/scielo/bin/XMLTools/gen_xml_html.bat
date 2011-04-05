
set JAVA_EXE=java

set XML_TOOLS_PATH=%1
set XML_FILENAM=%2
set XSL_XML=%3
set XSL_HTML=%4
set ERR_FILENAME=%5
set OUTPUT_XML=%6
set OUTPUT_HTML=%7
set ISSUE_PATH=%8
set FILENAME=%9

set LOG_FILE=%XML_FILENAM%.log
set TEMP_ERRFILE=%XML_FILENAM%.err

set XSL_RENAME_IMG=%XML_TOOLS_PATH%\rename_img.xsl

set TEMP_FILE=%TMP%\mkpmc_%time:~3,2%%time:~6,2%%time:~9,2%_0
set TEMP_FILE2=%TMP%\mkpmc_%time:~3,2%%time:~6,2%%time:~9,2%_2
set TEMP_OUTPUT_XML=%TMP%\mkpmc_%time:~3,2%%time:~6,2%%time:~9,2%_3
set TMP_SH_FILE=%XML_FILENAM%.bat

if exist %TEMP_FILE%    del /F %TEMP_FILE%
if exist %LOG_FILE%     del /F %LOG_FILE%
if exist %ERR_FILENAME% del /F %ERR_FILENAME%
if exist %OUTPUT_XML%   del /F %OUTPUT_XML%
if exist %OUTPUT_HTML%  del /F %OUTPUT_HTML%
if exist %TEMP_ERRFILE% del /F %TEMP_ERRFILE%
if exist %TEMP_FILE%    del /F %TEMP_FILE%
if exist %TMP_SH_FILE%  del /F %TMP_SH_FILE%

echo %date% %time% inicio >> %LOG_FILE%

rem 
rem PASSO 1 VALIDATE INPUT
rem
echo %date% %time% Passo 1 Validate %XML_FILENAM%  >> %LOG_FILE%
%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %XML_FILENAM%  > %TEMP_FILE%
if not exist %TEMP_FILE% echo validation error %XML_FILENAM% > %TEMP_ERRFILE%

if exist %TEMP_FILE% %XML_TOOLS_PATH%\..\cfg\mx seq=%TEMP_FILE% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_FILE% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%


if exist %TEMP_ERRFILE% goto ERR_VALIDATE


rem 
rem PASSO 2 TRANSFORMATION
rem
echo %date% %time% Passo 2 Transform %XML_FILENAM% %XSL_XML%  >> %LOG_FILE%

if exist %TEMP_FILE% del /F %TEMP_FILE%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %XML_FILENAM% %XSL_XML% 

if not exist %TEMP_FILE% echo PASSO 2 Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_FILE% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %XML_FILENAM% %XSL_XML% >> %TEMP_ERRFILE%
if not exist %TEMP_FILE% goto ERR_TRANSF

:COPY_XML
echo copying %OUTPUT_XML%
if exist %TEMP_FILE% copy %TEMP_FILE% %OUTPUT_XML%
if not exist %OUTPUT_XML% goto COPY_XML


rem 
rem PASSO 3 VALIDATE XML
rem
echo %date% %time% Passo 3 Validate %OUTPUT_XML%  >> %LOG_FILE%

if exist %TEMP_FILE% del /F %TEMP_FILE%


copy %OUTPUT_XML% %TEMP_FILE2%

echo %date% %time% %TEMP_FILE2% %TEMP_OUTPUT_XML%>>%LOG_FILE%
echo %date% %time% change to local dtd >>%LOG_FILE%

%XML_TOOLS_PATH%\..\cfg\mx mfrl=32000 seq=%TEMP_FILE2% lw=9999 "pft=if v1:'journalpublishing3.dtd' then replace(v1,'http://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd',s('file:///',replace('%XML_TOOLS_PATH%','\','/'),'/../markup/pmc/v3.0/dtd/publishing/journalpublishing3.dtd')),else v1 fi" now > %TEMP_OUTPUT_XML%

echo %date% %time% changed >>%LOG_FILE%

echo %date% %time% validating locally >>%LOG_FILE%

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %TEMP_OUTPUT_XML% --validate  > %TEMP_FILE%
echo %date% %time% validated >>%LOG_FILE%

if not exist %TEMP_FILE% echo validation error %OUTPUT_XML% > %TEMP_ERRFILE%

if exist %TEMP_FILE% %XML_TOOLS_PATH%\..\cfg\mx seq=%TEMP_FILE% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_FILE% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%

if exist %TEMP_ERRFILE% goto ERR_VALIDATE



rem 
rem PASSO 4 TRANSFORMATION
rem
echo %date% %time% Passo 4 Transform %OUTPUT_XML% %XSL_HTML% >> %LOG_FILE%

set TEMP_FILE=%TMP%\mkpmc_%time:~3,2%%time:~6,2%%time:~9,2%

if exist %TEMP_FILE% del /F %TEMP_FILE%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_OUTPUT_XML% %XSL_HTML% 

if not exist %TEMP_FILE% echo PASSO 4 Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_FILE% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_OUTPUT_XML% %XSL_HTML% >> %TEMP_ERRFILE%
if not exist %TEMP_FILE% goto ERR_TRANSF

:COPY_HTML
echo copying %OUTPUT_HTML%
if exist %TEMP_FILE% copy %TEMP_FILE% %OUTPUT_HTML%
if not exist %OUTPUT_HTML% goto COPY_HTML

rem 
rem PASSO 5 TRANSFORMATION
rem
echo %date% %time% Passo 5 Transform %XML_FILENAM% %XSL_RENAME_IMG% >> %LOG_FILE%
if exist %TEMP_FILE% del /F %TEMP_FILE%
%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %XML_FILENAM% %XSL_RENAME_IMG% 
if exist %TEMP_FILE% call %XML_TOOLS_PATH%\rename_files.bat %XML_TOOLS_PATH% %TEMP_FILE% %ISSUE_PATH% %OUTPUT_XML% %FILENAME%
if exist %TEMP_FILE% del /F %TEMP_FILE%

goto END

:ERR_TRANSF
echo %date% %time% ERR_TRANSF >> %LOG_FILE%
if exist %TEMP_ERRFILE% copy %TEMP_ERRFILE% %ERR_FILENAME%
goto END


:ERR_VALIDATE
echo %date% %time% ERR_VALIDATE >> %LOG_FILE%
if exist %TEMP_ERRFILE% copy %TEMP_ERRFILE% %ERR_FILENAME%
goto END


:END
if exist %TEMP_FILE%  del %TEMP_FILE%
if exist %TEMP_FILE2% del %TEMP_FILE2%
if exist %TEMP_OUTPUT_XML% del %TEMP_OUTPUT_XML%

echo %date% %time% fim >> %LOG_FILE%
