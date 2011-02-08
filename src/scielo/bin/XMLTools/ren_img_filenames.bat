set XML_TOOLS_PATH=%1
set src_img=%2
set dest_img=%3
set this2that=%4

set dest_temp=%dest_img%_temp
set temp_batch=%XML_TOOLS_PATH%\temp.bat

if not exist %dest_img%  mkdir %dest_img%
if not exist %dest_temp%  mkdir %dest_temp%


if exist %dest_img% %XML_TOOLS_PATH%\..\cfg\mx seq=%this2that% lw=9999 "proc='d9999a9999{',replace('%src_img%','_src',''),'{'" "pft=if p(v1) and p(v2) then 'if exist %src_img%\'v1'.tif copy %src_img%\'v1'.tif %dest_img%\'v2'.tif',#,'if exist %src_img%\'v1'.tif copy %src_img%\'v1'.tif %dest_temp%\'v1'-'v2'.tif',#,'if exist %src_img%\'v1'.tiff copy %src_img%\'v1'.tiff %dest_img%\'v2'.tif',#,'if exist %src_img%\'v1'.tiff copy %src_img%\'v1'.tiff %dest_temp%\'v1'-'v2'.tif',#,'if exist ',v9999,'\'v1'.jpg copy 'v9999'\'v1'.jpg 'v9999'\'v2'.jpg',# fi" now > %temp_batch%
if exist %temp_batch% call %temp_batch% 





