set file=%1
set report=%2
set fix=%3

if exist %file%.eps goto END
if exist %file%.tif goto END
if exist %file%.tiff goto END

echo %file%>> %report%

:END