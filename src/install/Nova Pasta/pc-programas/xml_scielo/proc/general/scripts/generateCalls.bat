@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%


set scilista=%1
set destination=%2

%MX% "seq=%scilista% " lw=9999 "pft=if p(v1) then 'call scripts\generateXML.bat %destination% ',v1,' ',v2,' ',v3,' ',v4/ fi" now> temp\generateXML.bat

call temp\generateXML.bat
