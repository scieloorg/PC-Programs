@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%
%JAVA_TRANSFORMATION% -jar %XML_SCIELO_PROGRAM_PATH%\..\bin\jar\saxonb9-1-0-8j\saxon9.jar -novw -w0 %1 %2 > %3