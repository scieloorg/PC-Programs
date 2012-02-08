
set JAVA_EXE=java

set PATH_XML_TOOLS=%1
set FILE_SGM_XML=%2
set XSL_SGML2XML_LOCALVALIDATION=%3
set PATH_XSL=%4
set ERR_FILENAME=%5
set OUTPUT_XML=%6
set OUTPUT_REPORT=%7
set ISSUE_PATH=%8
set FILENAME=%9

set XSL_SGML2XML=%PATH_XSL%\..\sgml2xml\sgml2pmc.xsl
set XSL_SGML2XML_LOCALVALIDATION=%PATH_XSL%\..\sgml2xml\sgml2pmc4localvalidation.xsl
set XSL_ERR=%PATH_XSL%\pmcstylechecker.xsl
set XSL_REPORT=%PATH_XSL%\pmcstylereporter.xsl
set XSL_RENAME_IMG=%PATH_XML_TOOLS%\rename_img.xsl

set LOG_FILE=%FILE_SGM_XML%.log
set TEMP_ERRFILE=%FILE_SGM_XML%.tmp.err
set OUTPUT_HTML=%OUTPUT_XML%.html

set TEMP_FILE1=%FILE_SGM_XML%.01.tmp
set TEMP_FILE2=%FILE_SGM_XML%.02.tmp
set TEMP_FILE3=%FILE_SGM_XML%.03.tmp
set TEMP_FILE4=%FILE_SGM_XML%.04.tmp
set TEMP_FILE5=%FILE_SGM_XML%.05.tmp
set TEMP_FILE6=%FILE_SGM_XML%.06.tmp
set TEMP_FILE7=%FILE_SGM_XML%.07.tmp
set TEMP_FILE8=%FILE_SGM_XML%.08.tmp
set TEMP_FILE9=%FILE_SGM_XML%.09.tmp
set OUTPUT_XML_LOCAL=%FILE_SGM_XML%.local.xml
set FILE_XML4REPORT=%FILE_SGM_XML%.rep.xml
set TMP_SH_FILE=%FILE_SGM_XML%.bat

if exist %ERR_FILENAME% del /F %ERR_FILENAME%
if exist %OUTPUT_XML%   del /F %OUTPUT_XML%
if exist %OUTPUT_REPORT%  del /F %OUTPUT_REPORT%


if exist %LOG_FILE%     del /F %LOG_FILE%
if exist %OUTPUT_HTML%   del /F %OUTPUT_HTML%

if exist %TEMP_ERRFILE%     del /F %TEMP_ERRFILE%

if exist %TEMP_FILE1% del /F %TEMP_FILE1%
if exist %TEMP_FILE2%   del /F %TEMP_FILE2%
if exist %TEMP_FILE3%   del /F %TEMP_FILE3%
if exist %TEMP_FILE4%   del /F %TEMP_FILE4%
if exist %TEMP_FILE5%   del /F %TEMP_FILE5%
if exist %TEMP_FILE6%   del /F %TEMP_FILE6%
if exist %TEMP_FILE7%   del /F %TEMP_FILE7%
if exist %TEMP_FILE8%   del /F %TEMP_FILE8%
if exist %TEMP_FILE9%   del /F %TEMP_FILE9%

if exist %TMP_SH_FILE%  del /F %TMP_SH_FILE%

echo %date% %time% inicio >> %LOG_FILE%


rem 
rem PASSO 1 VALIDATE sgm.xml
rem
set XML=%FILE_SGM_XML%
set TEMP_RESULT=%TEMP_FILE1%
echo %date% %time% Passo 1 Validate %XML%  >> %LOG_FILE%
%JAVA_EXE% -cp %PATH_XML_TOOLS%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %XML%  > %TEMP_RESULT%
if not exist %TEMP_RESULT%  echo validation error %XML% > %TEMP_ERRFILE%
if exist %TEMP_RESULT%   %PATH_XML_TOOLS%\..\cfg\mx seq=%TEMP_RESULT% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_RESULT% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%
if exist %TEMP_ERRFILE% goto ERR_VALIDATE

rem 
rem PASSO 2 TRANSFORM sgm.xml xml
rem
set TEMP_RESULT=%TEMP_FILE2%
set XML=%FILE_SGM_XML%
set XSL=%XSL_SGML2XML_LOCALVALIDATION% 
set RESULT=%OUTPUT_XML_LOCAL%
echo %date% %time% Passo 2 Transform %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 2 Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%

rem 
rem PASSO 3 VALIDATE xml
rem

set XML=%OUTPUT_XML_LOCAL%
set TEMP_RESULT=%TEMP_FILE3%
echo %date% %time% Passo 3 Validate %XML%  >> %LOG_FILE%
%JAVA_EXE% -cp %PATH_XML_TOOLS%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %XML%  > %TEMP_RESULT%
if not exist %TEMP_RESULT%  echo validation error %XML% > %TEMP_ERRFILE%
if exist %TEMP_RESULT%   %PATH_XML_TOOLS%\..\cfg\mx seq=%TEMP_RESULT% lw=9999 "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %TEMP_RESULT% %TEMP_ERRFILE%'/ fi" now > %TMP_SH_FILE%
if exist %TMP_SH_FILE% call %TMP_SH_FILE%
if exist %TMP_SH_FILE% del /F %TMP_SH_FILE%
if exist %TEMP_ERRFILE% goto ERR_VALIDATE


rem 
rem PASSO 4a TRANSFORM xml 2 report.xml
rem
set TEMP_RESULT=%TEMP_FILE4%
set XML= %OUTPUT_XML_LOCAL%
set XSL=%XSL_ERR%
set RESULT=%FILE_XML4REPORT%
echo %date% %time% Passo 2 Transform %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 4a Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%

rem 
rem PASSO 4b TRANSFORMATION report.xml 2 report html
rem
set TEMP_RESULT=%TEMP_FILE5%
set XML= %FILE_XML4REPORT%
set XSL=%XSL_REPORT%
set RESULT=%OUTPUT_REPORT%
echo %date% %time% Passo 2 Transform %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 4a Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%

rem 
rem PASSO 5 TRANSFORMATION xml 2 html
rem
set TEMP_RESULT=%TEMP_FILE6%
set XML= %OUTPUT_XML_LOCAL%
set XSL=%PATH_XSL%\viewText.xsl
set RESULT=%OUTPUT_HTML%
echo %date% %time% Passo 2 Transform %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 4a Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%

rem 
rem PASSO 5b TRANSFORMATION xml 2 html
rem
set TEMP_RESULT=%TEMP_FILE7%
set XML=%FILE_SGM_XML%
set XSL=%XSL_SGML2XML%
set RESULT=%OUTPUT_XML%
echo %date% %time% Passo 5b Transform %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 4a Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%


rem 
rem PASSO 6 TRANSFORMATION RENAMING IMG
rem
set TEMP_RESULT=%TEMP_FILE8%
set XML=%FILE_SGM_XML%
set XSL=%XSL_RENAME_IMG%
set RESULT=%TEMP_FILE9%
echo %date% %time% PASSO 6 TRANSFORMATION RENAMING IMG %XML% %XSL%  >> %LOG_FILE%
if exist %TEMP_RESULT% del /F %TEMP_RESULT%
if exist %RESULT% del /F %RESULT%
%JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% 
if not exist %TEMP_RESULT% echo PASSO 4a Transformation error     > %TEMP_ERRFILE%
if not exist %TEMP_RESULT% echo %JAVA_EXE% -jar %PATH_XML_TOOLS%\core\saxon8.jar -novw -w0 -o %TEMP_RESULT% %XML% %XSL% >> %TEMP_ERRFILE%
if not exist %TEMP_RESULT% goto ERR_TRANSF
if exist %TEMP_RESULT% copy %TEMP_RESULT% %RESULT%
if exist %RESULT% call %PATH_XML_TOOLS%\rename_files.bat %PATH_XML_TOOLS% %RESULT% %ISSUE_PATH% %OUTPUT_XML% %FILENAME%

:DELETE_TEMP_FILES
goto END
if exist %TEMP_ERRFILE%     del /F %TEMP_ERRFILE%

if exist %TEMP_FILE1% del /F %TEMP_FILE1%
if exist %TEMP_FILE2%   del /F %TEMP_FILE2%
if exist %TEMP_FILE3%   del /F %TEMP_FILE3%
if exist %TEMP_FILE4%   del /F %TEMP_FILE4%
if exist %TEMP_FILE5%   del /F %TEMP_FILE5%
if exist %TEMP_FILE6%   del /F %TEMP_FILE6%
if exist %TEMP_FILE7%   del /F %TEMP_FILE7%
if exist %TEMP_FILE8%   del /F %TEMP_FILE8%
if exist %TEMP_FILE9%   del /F %TEMP_FILE9%

if exist %TMP_SH_FILE%  del /F %TMP_SH_FILE%
goto END

:ERR_TRANSF
echo %date% %time% ERR_TRANSF >> %LOG_FILE%
rem if exist %TEMP_ERRFILE% copy %TEMP_ERRFILE% %ERR_FILENAME%
more %TEMP_ERRFILE% >> %LOG_FILE%
copy %LOG_FILE% %ERR_FILENAME%
goto END


:ERR_VALIDATE
echo %date% %time% ERR_VALIDATE >> %LOG_FILE%
rem if exist %TEMP_ERRFILE% copy %TEMP_ERRFILE% %ERR_FILENAME%
more %TEMP_ERRFILE% >> %LOG_FILE% 
copy %LOG_FILE% %ERR_FILENAME%
goto END


:END



echo %date% %time% fim >> %LOG_FILE%
