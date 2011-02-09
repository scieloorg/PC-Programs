set THIS=%1
set THAT=%2
set IMG_SRC=%3
set IMG=%4
set PMC=%5
set PMC_TEMP=%6

rem RENOMEIA IMAGEM ORIGINAL TIFF PARA PMC

if exist %IMG_SRC%\%THIS%.tif  copy %IMG_SRC%\%THIS%.tif  %PMC%\%THAT%.tif
if exist %IMG_SRC%\%THIS%.tiff copy %IMG_SRC%\%THIS%.tiff %PMC%\%THAT%.tif

if exist %IMG_SRC%\%THIS%.tif  copy %IMG_SRC%\%THIS%.tif  %PMC_TEMP%\%THAT%_ALIAS_%THIS%.tif
if exist %IMG_SRC%\%THIS%.tiff copy %IMG_SRC%\%THIS%.tiff %PMC_TEMP%\%THAT%_ALIAS_%THIS%.tif


rem RENOMEIA IMAGEM ORIGINAL JPG PARA IMG

if exist %IMG_SRC%\%THIS%.jpg copy %IMG_SRC%\%THIS%.jpg %IMG%\%THAT%.jpg
if exist %IMG%\%THIS%.jpg     copy %IMG%\%THIS%.jpg     %IMG%\%THAT%.jpg


