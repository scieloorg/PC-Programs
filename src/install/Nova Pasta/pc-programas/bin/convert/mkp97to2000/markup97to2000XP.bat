@echo off
rem markup97to2000XP.bat
rem Parameter 1: input file
rem Parameter 2: output file
rem
rem This batch file removes some html tags which 
rem cause conversion problems on SciELO Converter Program.
rem

rem Initializing variables
rem set PRGS_DIR=./
set PRGS_DIR=mkp97to2000\
set SEARCH_EXPR_TR="\n\r"
set SEARCH_EXPR_SED_STEP1="s/<span[^>]*>//g"
set SEARCH_EXPR_SED_STEP2="s/<[/]span>//g"

rem Step 1 for removing Carriage Return
call %PRGS_DIR%tr %SEARCH_EXPR_TR% " " < %1 > %1.tmp

rem Step 2 for removing span tags
if "%1"=="%2" copy %1 %1.old > nul
call %PRGS_DIR%sed -e %SEARCH_EXPR_SED_STEP1% -e %SEARCH_EXPR_SED_STEP2% %1.tmp > %2 
del %1.tmp
