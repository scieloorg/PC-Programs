set THIS=%1
set THAT=%2
set PMC=%3
set PMC_TEMP=%4
set IMG_SRC=%5
set IMG=%6
set XML_TOOLS_PATH=%7

rem RENOMEIA IMAGEM ORIGINAL TIFF PARA PMC


if exist %IMG_SRC%\%THIS%.tif  copy %IMG_SRC%\%THIS%.tif   %PMC%\%THAT%.tif
if exist %IMG_SRC%\%THIS%.tiff copy %IMG_SRC%\%THIS%.tiff  %PMC%\%THAT%.tif
if exist %IMG_SRC%\%THIS%.eps copy %IMG_SRC%\%THIS%.eps  %PMC%\%THAT%.eps

if exist %IMG%\%THIS%.jpg  copy %IMG%\%THIS%.jpg   %PMC_TEMP%\%THAT%.jpg




