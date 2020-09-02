@echo off
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ===== Executing %0 %1 %2 %3 %4 %5 %6 %7 %8 %9 >> %LOG%

set MX=%1
set EXPORT_TO=%2
set acron=%3
set issueid=%4
set generate_linkout=%5
set ahpdate=%6
set maxdate=%7

set mydb=%PATH_DB%\%acron%\%issueid%\base\%issueid%
set mydbinv=temp\%acron%_%issueid%

set mydbahead0=%PATH_DB%\%acron%\nahead\base\nahead
set mydbahead1=temp\%acron%_nahead
set mydbaheadinv=temp\%acron%_%issueid%

if exist %mydbahead0%.mst %MX% %mydbahead0% create=%mydbahead1% now -all
if exist %mydbahead1%.mst call batch\GeraInvertido.bat %mydbahead1% %FST% %mydbahead1% 


%MX% %mydb% create=%mydbinv% now -all
if not exist %mydb%.mst goto END_GENERATE_XML
call batch\GeraInvertido.bat %mydbinv% %FST% %mydbinv%

echo. > temp\xml_scielo_xsl.seq

echo Getting XSL list >> %LOG%
%WXIS% IsisScript=xis\xml_scielo_getXSL.xis acron=%acron% issueid=%issueid% generate_linkout=%generate_linkout% ahpdate=%ahpdate% cipar=%CIPAR_FILE% xslList=temp\xml_scielo_xsl.seq debug=%debug% destination=%EXPORT_TO% maxdate=%maxdate% >> %LOG%
more temp\xml_scielo_xsl.seq >> %LOG%

%MX% "seq=temp\xml_scielo_xsl.seq " lw=9999 "pft=if p(v2) and p(v3) then 'call scripts\applyXSL.bat ',v1,' ',v2,' ',v3,' %acron% %issueid% ',v4,| |v5,|  |v6,/ fi" now > temp\xml_scielo_transform_and_transfer.bat

echo Generating and transfering the XML file >> %LOG%
call temp\xml_scielo_transform_and_transfer.bat 

:END_GENERATE_XML
if not exist %mydb%.mst echo %mydb%.mst was not found. Failure.
if not exist %mydb%.mst echo %2 %3 >> %REPROCESSFALTADB%
echo End >> %LOG%