echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%
set xml=%1
set xsl=%2
set result=%3

echo Transforming %result% >> %LOG%

if not "@%JAVA_TRANSFORMATION%"=="@" goto JAVA_TRANSFORMATION

:PHP_TRANSFORMATION
call scripts\transformByPHP.bat %xml% %xsl% %result%
goto END_TRANSFORMATION
 
:JAVA_TRANSFORMATION
call scripts\transformByJava.bat %xml% %xsl% %result% 

rem more error_end.txt

:END_TRANSFORMATION

goto XXX


:XXX