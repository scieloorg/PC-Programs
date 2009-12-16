@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%
%JAVA_TRANSFORMATION% -jar %XML_SCIELO_PROGRAM_PATH%\proc\general\java\saxon8.jar -novw -w0 %1 %2 > %3