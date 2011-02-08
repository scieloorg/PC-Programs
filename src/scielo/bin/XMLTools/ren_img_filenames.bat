set XML_TOOLS_PATH=%1
set src_img=%2
set dest_img=%3
set this2that=%4


if not exist %dest_img%  mkdir %dest_img%


if exist %dest_img% %XML_TOOLS_PATH%\..\cfg\mx seq=%this2that% lw=9999 "pft=if p(v1) and p(v2) then 'if exist %src_img%\'v1,'.tif* copy %src_img%\'v1,'.tif* %dest_img%\',v2,'.tif',#,'if exist %src_img%\'v1,'.tif* copy %src_img%\'v1,'.tif* %src_img%\',v1,'-',v2,'.tif',# fi" now > temp.bat
if exist temp.bat call temp.bat





