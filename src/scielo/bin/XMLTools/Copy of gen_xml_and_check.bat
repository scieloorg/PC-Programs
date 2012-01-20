
set JAVA_EXE=java

set PATH_XML_TOOLS=%1
set FILE_SGM_XML=%2
set FILE_XSL_SGM2XML=%3
set PATH_XSL=%4
set ERR_FILENAME=%5
set OUTPUT_XML=%6
set OUTPUT_REPORT=%7
set ISSUE_PATH=%8
set FILENAME=%9

set XSL_ERR=%PATH_XSL%\pmcstylechecker.xsl
set XSL_REPORT=%PATH_XSL%\pmcstylereporter.xsl

set LOG_FILE=%FILE_SGM_XML%.log
set TEMP_ERRFILE=%FILE_SGM_XML%.tmp.err

set XSL_RENAME_IMG=%PATH_XML_TOOLS%\rename_img.xsl

set TEMP_FILE1=%FILE_SGM_XML%.01.tmp
set TEMP_FILE2=%FILE_SGM_XML%.02.tmp
set TEMP_FILE3=%FILE_SGM_XML%.03.tmp
set TEMP_FILE4=%FILE_SGM_XML%.04.tmp
set TEMP_FILE5=%FILE_SGM_XML%.05.tmp
set TEMP_FILE6=%FILE_SGM_XML%.06.tmp

set OUTPUT_HTML=%OUTPUT_XML%.html
set OUTPUT_XML_LOCAL=%FILE_SGM_XML%.local.xml
set FILE_XML4REPORT=%FILE_SGM_XML%.rep.xml
set TMP_SH_FILE=%FILE_SGM_XML%.bat



if exist %TEMP_FILE%    del /F %TEMP_FILE%
if exist %LOG_FILE%     del /F %LOG_FILE%
if exist %ERR_FILENAME% del /F %ERR_FILENAME%
if exist %OUTPUT_XML%   del /F %OUTPUT_XML%
if exist %OUTPUT_REPORT%  del /F %OUTPUT_REPORT%
if exist %TEMP_ERRFILE% del /F %TEMP_ERRFILE%
if exist %TEMP_FILE%    del /F %TEMP_FILE%
if exist %TMP_SH_FILE%  del /F %TMP_SH_FILE%

echo %date% %time% inicio >> %LOG_FILE%

rem 
rem PASSO 1 VALIDATE sgm.xml
rem
echo %date% %time% Passo 1 Validate %FILE_SGM_XML%  >> %LOG_FILE%
set TEMP_FILE=%TEMP_FILE1%
%JAVA_EXE% -cp %PATH_XML_TOOLS%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %FILE_SGM_XML%  > %TEMP_FILE%

if not exist %TEMP_FILE%  echo validation error %FILE_SGM_XML% > %TEMP_ERRFILE%

if exist %TEMP_FILE%   %PATH_XML_TOOLS%\..\cfg\mx seq=%TEMP_FILE% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_FILE% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%

if exist %TEMP_ERRFILE% goto ERR_VALIDATE


rem 
rem PASSO 2 TRANSFORMATION sgm.xml xml
rem
echo %date% %time% Passo 2 Transform %FILE_SGM_XML% %FILE_XSL_SGM2XML%  >> %LOG_FILE%
set TEMP_FILE=%TEMP_FILE2%
if exist %TEMP_FILE% del /F %TEMP_FILE%

%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %FILE_SGM_XML% %FILE_XSL_SGM2XML% 

if exist %TEMP_FILE% echo copying %OUTPUT_XML%>> %LOG_FILE%
if exist %TEMP_FILE% copy %TEMP_FILE% %OUTPUT_XML%
if exist %TEMP_FILE% goto STEP3

echo PASSO 2 Transformation error     > %TEMP_ERRFILE%
echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %FILE_SGM_XML% %FILE_XSL_SGM2XML% >> %TEMP_ERRFILE%
goto ERR_TRANSF

:STEP3
rem 
rem PASSO 3 VALIDATE xml
rem
echo %date% %time% Passo 3 Validate %OUTPUT_XML%  >> %LOG_FILE%
set TEMP_FILE=%TEMP_FILE3%
if exist %TEMP_FILE% del /F %TEMP_FILE%
set XML_TMP=%OUTPUT_XML% 

echo %date% %time% %TEMP_FILE2% %OUTPUT_XML_LOCAL%>>%LOG_FILE%
echo %date% %time% change to local dtd >>%LOG_FILE%

%PATH_XML_TOOLS%\..\cfg\mx mfrl=32000 fmtl=32000 seq=%XML_TMP%  lw=9999 "pft=if v1:'journalpublishing3.dtd' then replace(v1,'http://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd',s('file:///',replace('%PATH_XML_TOOLS%','\','/'),'/../markup/pmc/v3.0/dtd/publishing/journalpublishing3.dtd')),else v1,if p(v2) then '|'v2 fi fi" now > %OUTPUT_XML_LOCAL%
echo %date% %time% changed >>%LOG_FILE%
echo %date% %time% validating locally %OUTPUT_XML_LOCAL%>>%LOG_FILE%
%JAVA_EXE% -cp %PATH_XML_TOOLS%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %OUTPUT_XML_LOCAL% --validate  > %TEMP_FILE%

if not exist %TEMP_FILE% echo validation error %OUTPUT_XML_LOCAL% > %TEMP_ERRFILE%

if exist %TEMP_FILE% %PATH_XML_TOOLS%\..\cfg\mx seq=%TEMP_FILE% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_FILE% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%

if exist %TEMP_ERRFILE% goto ERR_VALIDATE

rem 
rem PASSO 4 TRANSFORMATION xml 2 report.xml
rem
echo %date% %time% Passo 4 Transform %OUTPUT_XML_LOCAL% %XSL_ERR% >> %LOG_FILE%

set TEMP_FILE=%FILE_XML4REPORT%
set TEMP_XML=%OUTPUT_XML_LOCAL%
if exist %TEMP_FILE% del /F %TEMP_FILE%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_XML% %XSL_ERR% 

if not exist %TEMP_FILE% echo PASSO 4 Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_FILE% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_XML% %XSL_ERR% >> %TEMP_ERRFILE%
if not exist %TEMP_FILE% goto ERR_TRANSF

rem 
rem PASSO 5 TRANSFORMATION xml 2 report
rem
echo %date% %time% Passo 5 Transform %TEMP_FILE% %XSL_REPORT% >> %LOG_FILE%
copy  %TEMP_FILE% %FILE_XML4REPORT%

set TEMP_FILE=%TEMP_FILE5%
if exist %TEMP_FILE% del /F %TEMP_FILE%

%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %FILE_XML4REPORT% %XSL_REPORT% 

if exist %TEMP_FILE% copy %TEMP_FILE% %OUTPUT_REPORT%


if not exist %TEMP_FILE% echo PASSO 5 Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_FILE% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %FILE_XML4REPORT% %XSL_REPORT% >> %TEMP_ERRFILE%
if not exist %TEMP_FILE% goto ERR_TRANSF

rem 
rem PASSO 5b TRANSFORMATION xml 2 html
rem
set XSL_HTML=%PATH_XSL%\viewText.xsl
set TEMP_FILE5b=%OUTPUT_XML_LOCAL% 
echo %date% %time% Passo 5b Transform %TEMP_FILE5b% %XSL_HTML% >> %LOG_FILE%

if exist %TEMP_FILE% del /F %TEMP_FILE%
echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_FILE5b% %XSL_HTML% >> %LOG_FILE%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_FILE5b% %XSL_HTML% 
if exist %TEMP_FILE% copy %TEMP_FILE% %OUTPUT_HTML%


if not exist %TEMP_FILE% echo PASSO 5b Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_FILE% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %TEMP_FILE5b% %XSL_HTML%  >> %TEMP_ERRFILE%
if not exist %TEMP_FILE% goto ERR_TRANSF


rem 
rem PASSO 6 TRANSFORMATION RENAMING IMG
rem
echo %date% %time% Passo 6 Transform %FILE_SGM_XML% %XSL_RENAME_IMG% >> %LOG_FILE%
set TEMP_FILE=%TEMP_FILE6%
if exist %TEMP_FILE% del /F %TEMP_FILE%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_FILE% %FILE_SGM_XML% %XSL_RENAME_IMG% 
if exist %TEMP_FILE% call %PATH_XML_TOOLS%\rename_files.bat %PATH_XML_TOOLS% %TEMP_FILE% %ISSUE_PATH% %OUTPUT_XML% %FILENAME%
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

echo %date% %time% fim >> %LOG_FILE%
