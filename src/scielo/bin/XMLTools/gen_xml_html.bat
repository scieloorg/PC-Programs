
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


SET XSL_RENAME_IMG=%XML_TOOLS_PATH%\rename_img.xsl

set temp_errfile=%XML_FILENAM%.err
set temp_file=%XML_FILENAM%.tmp
set log_file=%XML_FILENAM%.log
set temp_sh_file=%XML_FILENAM%.bat

if exist %log_file% del %log_file%


if exist %ERR_FILENAME% del %ERR_FILENAME%
if exist %OUTPUT_XML%   del %OUTPUT_XML%
if exist %OUTPUT_HTML%  del %OUTPUT_HTML%

if exist %temp_errfile% del %temp_errfile%
if exist %temp_file%    del %temp_file%
if exist %temp_sh_file% del %temp_sh_file%

rem 
rem PASSO 1 VALIDATE INPUT
rem
echo Validate %XML_FILENAM%  >> %log_file%
%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %XML_FILENAM%  > %temp_file%
if not exist %temp_file% echo validation error %XML_FILENAM% > %temp_errfile%

if exist %temp_file% %XML_TOOLS_PATH%\..\cfg\mx seq=%temp_file% "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %temp_file% %temp_errfile%'/ fi" now > %temp_sh_file%
if exist %temp_sh_file% call %temp_sh_file%

if exist %temp_errfile% goto ERR_VALIDATE


rem 
rem PASSO 2 TRANSFORMATION
rem
echo Transform %XML_FILENAM% %XSL_XML%  >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %XML_FILENAM% %XSL_XML% 

if not exist %temp_file% echo Transformation error     > %temp_errfile%
if not exist %temp_file% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %XML_FILENAM% %XSL_XML% >> %temp_errfile%
if not exist %temp_file% goto ERR_TRANSF


if exist %temp_file% copy %temp_file% %OUTPUT_XML%


rem 
rem PASSO 3 VALIDATE XML
rem
echo Validate %OUTPUT_XML%  >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %OUTPUT_XML% --validate  > %temp_file%
if not exist %temp_file% echo validation error %OUTPUT_XML% > %temp_errfile%

if exist %temp_file% %XML_TOOLS_PATH%\..\cfg\mx seq=%temp_file% "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %temp_file% %temp_errfile%'/ fi" now > %temp_sh_file%
if exist %temp_sh_file% call %temp_sh_file%

if exist %temp_errfile% goto ERR_VALIDATE



rem 
rem PASSO 4 TRANSFORMATION
rem
echo Transform %OUTPUT_XML% %XSL_HTML% >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %OUTPUT_XML% %XSL_HTML% 

if not exist %temp_file% echo Transformation error     > %temp_errfile%
if not exist %temp_file% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %XML_FILENAM% %XSL_XML% >> %temp_errfile%
if not exist %temp_file% goto ERR_TRANSF

if exist %temp_file% copy %temp_file% %OUTPUT_HTML%


rem 
rem PASSO 5 TRANSFORMATION
rem
echo Transform %XML_FILENAM% %XSL_RENAME_IMG% >> %log_file%
if exist %temp_file% del %temp_file%
%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %XML_FILENAM% %XSL_RENAME_IMG% 
if exist %temp_file% call %XML_TOOLS_PATH%\rename_files.bat %XML_TOOLS_PATH% %temp_file% %ISSUE_PATH% %OUTPUT_XML% %FILENAME%
if exist %temp_file% del %temp_file%

goto END

:ERR_TRANSF
if exist %temp_errfile% copy %temp_errfile% %ERR_FILENAME%
goto END


:ERR_VALIDATE
if exist %temp_errfile% copy %temp_errfile% %ERR_FILENAME%
goto END


:END

