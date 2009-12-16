set mx=%1
set db=%2
set cfg_gen=%3
set cfg_en=%4

set cfg_es=%5
set cfg_pt=%6

echo %cfg_gen%
%mx% %db% btell=0 "bool=gen" lw=999 "pft=if size(v1)>0 then v1,',',v2,',',v3,',',v4/ fi" now > %cfg_gen%

%mx% %db% btell=0 "bool=gen" lw=999 "proc='a10{en{'" "pft=@cfg.pft" now > %cfg_en%
%mx% %db% btell=0 "bool=gen" lw=999 "proc='a10{es{'" "pft=@cfg.pft" now > %cfg_es%
%mx% %db% btell=0 "bool=gen" lw=999 "proc='a10{pt{'" "pft=@cfg.pft" now > %cfg_pt%

