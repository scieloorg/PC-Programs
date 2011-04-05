set IMG_SRC_PATH=%1
set IMG_PATH=%2
set mx=%3
set result=%4

if exist %result% del %result%
dir /b/s %IMG_PATH% > %IMG_PATH%_00.txt
%mx% seq=%IMG_PATH%_00.txt lw=9999 "pft=if instr(v1,'.jpg')>0 then mid(v1,1,size(v1)-4)/ fi" now > %IMG_PATH%_01.txt
%mx% seq=%IMG_PATH%_01.txt lw=9999 "pft='call check_img_file.bat ',replace(v1,'\img','\img_src'),' %result% ',/" now > %IMG_PATH%_02.bat

call %IMG_PATH%_02.bat

if exist %result% echo Problems are reported in %result%


