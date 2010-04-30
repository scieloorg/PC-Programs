@echo off

cls
echo Este programa vai exportar os dados da title, section e issue, de uma lista de acronimos
echo Um arquivo ira abrir. Escreva nele uma lista de acronimos, em letras minusculas, dos periodicos a serem exportados
echo   Tecle CONTROL-C para sair ou ENTER para continuar...

pause > nul

call notepad temp\title.lst
cls
echo -----------------------
echo Serao gerados os dados de
more temp\title.lst
echo -----------------------
echo   Tecle CONTROL-C para sair ou ENTER para continuar...
pause > nul
cls
echo Aguarde ....

cisis\mx seq=..\bin\scielo_paths.ini lw=9999 "pft=if v1:'=' then replace(v1,',','=')/ fi" now > temp\scielo_paths.seq

cisis\mx "seq=temp\scielo_paths.seq=" create=temp\scielo_paths now -all
cisis\mx temp\scielo_paths "fst=1 0 mpl,v1/" fullinv=temp\scielo_paths

if not exist temp md temp
if not exist temp\serial md temp\serial
if not exist temp\serial\title md temp\serial\title
if not exist temp\serial\section md temp\serial\section
if not exist temp\serial\issue md temp\serial\issue

cisis\mx null count=0 create=temp\serial\title\title now -all
cisis\mx null count=0 create=temp\serial\section\section now -all
cisis\mx null count=0 create=temp\serial\issue\issue now -all



cisis\mx "seq=temp\title.lst" lw=9999 "pft='call scripts\ExportSerial_append.bat ',ref(['temp\scielo_paths']l(['temp\scielo_paths']'Serial Directory'),v2),' ',v1,' ',mpu,v1,mpl/" now > temp\ExportSerial_append.bat 
call temp\ExportSerial_append.bat 

cisis\mx null count=1 lw=9999 "pft='call scripts\ExportSerial_Invert.bat ',ref(['temp\scielo_paths']l(['temp\scielo_paths']'Serial Directory'),v2),#" now > temp\ExportSerial_invert.bat
call temp\ExportSerial_invert.bat 

echo -----------------------
echo  DADOS GERADOS EM temp\serial
echo -----------------------
