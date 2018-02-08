@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%
set receptorName=%1
set acron=%2
set issueid=%3
set filename=%4
set fname=%5

if not exist %filename% goto NOT_GENERATED

echo Copying %filename% to >> %LOG%
echo    %PATH_DB%\%receptorName% >> %LOG%
echo    %PATH_DB%\%acron%\%receptorName% >> %LOG%
echo    %PATH_DB%\%acron%\%issueid%\%receptorName% >> %LOG%

if not exist %PATH_DB%\%receptorName%\ mkdir %PATH_DB%\%receptorName%\
if not exist %PATH_DB%\%acron%\%receptorName%\ mkdir %PATH_DB%\%acron%\%receptorName%\
if not exist %PATH_DB%\%acron%\%issueid%\%receptorName%\ mkdir %PATH_DB%\%acron%\%issueid%\%receptorName%\

copy /y %filename% %PATH_DB%\%receptorName%\%fname% >> %LOG%
copy /y %filename% %PATH_DB%\%acron%\%receptorName%\%fname% >> %LOG%
copy /y %filename% %PATH_DB%\%acron%\%issueid%\%receptorName%\%fname% >> %LOG%


if exist %PATH_DB%\%receptorName%\%fname% echo  Generated %PATH_DB%\%receptorName%\%fname%
rem if exist %PATH_DB%\%receptorName%\%fname% dir %PATH_DB%\%receptorName%\%fname%

if not exist %PATH_DB%\%receptorName%\%fname% echo  NOT generated %PATH_DB%\%receptorName%\%fname%

goto END


:NOT_GENERATED
echo  NOT generated %PATH_DB%\%receptorName%\%fname%


:END