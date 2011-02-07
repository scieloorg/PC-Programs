
set JAVA_EXE=%1
set XML_TOOLS_PATH=%2
set xml_filename=%3
set xsl_xml=%4
set xsl_html=%5

set err_file=%6
set output_xml=%7
set output_html=%8


set temp_errfile=%xml_filename%.err
set temp_file=%xml_filename%.tmp
set log_file=%xml_filename%.log
set temp_sh_file=%xml_filename%.bat

if exist %log_file% del %log_file%
if exist %temp_errfile% del %temp_errfile%
if exist %output_xml% del %output_xml%
if exist %output_html% del %output_html%
if exist %temp_file% del %temp_file%
if exist %temp_sh_file% del %temp_sh_file%

rem 
rem PASSO 1 VALIDATE INPUT
rem
echo Validate %xml_filename%  >> %log_file%
%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %xml_filename%  > %temp_file%
if not exist %temp_file% echo validation error %xml_filename% > %temp_errfile%

if exist %temp_file% %XML_TOOLS_PATH%\..\cfg\mx seq=%temp_file% "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %temp_file% %temp_errfile%' fi" now > %temp_sh_file%
if exist %temp_sh_file% call %temp_sh_file%

if exist %temp_errfile% goto ERR_VALIDATE


rem 
rem PASSO 2 TRANSFORMATION
rem
echo Transform %xml_filename% %xsl_xml%  >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %xml_filename% %xsl_xml% 

if not exist %temp_file% echo Transformation error     > %temp_errfile%
if not exist %temp_file% echo %0 %1 %2 %3 %4 %5 %6 %7  >> %temp_errfile%
if not exist %temp_file% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %xml_filename% %xsl_xml% >> %temp_errfile%
if not exist %temp_file% goto ERR_TRANSF


if exist %temp_file% copy %temp_file% %output_xml%


rem 
rem PASSO 3 VALIDATE XML
rem
echo Validate %output_xml%  >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -cp %XML_TOOLS_PATH%\core\XMLCheck.jar br.bireme.XMLCheck.XMLCheck %output_xml% --validate  > %temp_file%
if not exist %temp_file% echo validation error %output_xml% > %temp_errfile%

if exist %temp_file% %XML_TOOLS_PATH%\..\cfg\mx seq=%temp_file% "pft=if s(mpu,v1,mpl):'ERROR' then 'copy %temp_file% %temp_errfile%' fi" now > %temp_sh_file%
if exist %temp_sh_file% call %temp_sh_file%

if exist %temp_errfile% goto ERR_VALIDATE



rem 
rem PASSO 4 TRANSFORMATION
rem
echo Transform %output_xml% %xsl_html% >> %log_file%

if exist %temp_file% del %temp_file%

%JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %output_xml% %xsl_html% 

if not exist %temp_file% echo Transformation error     > %temp_errfile%
if not exist %temp_file% echo %0 %1 %2 %3 %4 %5 %6 %7  >> %temp_errfile%
if not exist %temp_file% echo %JAVA_EXE% -jar %XML_TOOLS_PATH%\core\saxon8.jar -novw -w0 -o %temp_file% %xml_filename% %xsl_xml% >> %temp_errfile%
if not exist %temp_file% goto ERR_TRANSF


if exist %temp_file% copy %temp_file% %output_html%
goto END

:ERR_TRANSF
if exist %temp_errfile% copy %temp_errfile% %err_file%
goto END


:ERR_VALIDATE
if exist %temp_errfile% copy %temp_errfile% %err_file%
goto END


:END

