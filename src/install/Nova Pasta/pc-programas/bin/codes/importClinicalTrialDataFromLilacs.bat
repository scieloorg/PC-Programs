rem Parametro 1 mx
rem Parametro 2 base iso com os nomes das bases
rem Parametro 3 base code

@echo off
md temp
%1 iso=%2 lw=9999 "pft=if mfn=1 then '`d1d2','a1{ctdbid{' fi,'a2{^c',v2,'^v',v3,'{'," now> temp\clinicaltrial.prc 
echo ` >> temp\clinicaltrial.prc

%1 %3 text=ctdbid lw=9999 "pft='%1 %3 text=ctdbid proc=@temp\clinicaltrial.prc copy=%3 now -all'/" now > temp\clinicaltrial.txt
%1 %3 count=1 lw=9999 "pft='%1 %3 count=1 proc=@temp\clinicaltrial.prc append=%3 now -all'/" now >> temp\clinicaltrial.txt

%1 seq=temp\clinicaltrial.txt count=1 lw=9999 "pft=v1/" now > temp\clinicaltrial.bat

echo Checking the update
call temp\clinicaltrial.bat
%1 iso=%2 now 
%1 %3 text=ctdbid now