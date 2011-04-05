@echo off

set issue_path=%1
set app_path=%2


if "@%issue_path%" == "@" goto MISS01
if "@%app_path%" == "@"   goto MISS02

call check_img_files.bat %issue_path%\img_src %issue_path%\img %app_path%\bin\cfg\mx %issue_path%\pmc_work\missing_img.txt
goto END

:MISS01
echo "Parameter 1 is missing. It must be the issue path. E.g.: c:\scielo\serial\bjm\v41n2"
goto END

:MISS02
echo "Parameter 2 is missing. It must be the app path. E.g.: c:\scielo"
goto END


:END