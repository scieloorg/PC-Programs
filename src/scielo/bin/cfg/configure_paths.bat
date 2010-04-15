if exist %1\bin\scielo_paths.ini copy %1\bin\scielo_paths.ini %1\bin\scielo_paths.ini.old


%1\bin\cfg\mx seq=%1\bin\scielo_paths.example.ini lw=99999 "pft=replace(replace(replace(v1,'d:\dados\scielo','%2'),'c:\programas\scielo','%1'),'MYSCIELOURL','%3')/,#" now > %1\bin\scielo_paths.ini

%1\bin\cfg\mx seq=%1\bin\cfg\temp.txt lw=99999 "pft=replace(v1,'C:\SCIELO','%1'),#" now >  %1\bin\sgmlpars\settings.cfg


%1\bin\cfg\mx null count=1 "pft='`d9999a9999{',replace('%x%','\','/'),'{`'" now > x.txt

%1\bin\cfg\mx seq=%1\bin\markup\pmc\v3.0\sgml2xml\sgml2pmc4local.original.xsl lw=99999 "proc=@x.txt" "pft=replace(v1,'c:\programas\scielo',v9999),#" now > %1\bin\markup\pmc\v3.0\sgml2xml\sgml2pmc4localvalidation.xsl


if exist %2\serial\code\code.fst xcopy /K /Q /Y /O  %2\serial\code\code.fst %2\serial\code\newcode.fst

if exist %2\serial\code\newcode.mst goto FIM
if exist %2\serial\code\code.mst xcopy /K /Q /Y /O %2\serial\code\code.* %2\serial\code\newcode.*

:FIM

if exist %2\serial\code\code.mst %1\bin\cfg\mx %2\serial\code\code fst=@ fullinv=%2\serial\code\code
if exist %2\serial\code\newcode.mst %1\bin\cfg\mx %2\serial\code\newcode fst=@ fullinv=%2\serial\code\newcode

SET BAP=OS23470a

