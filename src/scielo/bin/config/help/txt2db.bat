set mx=%1
set db=%2
set txt_gen=%3
set txt_lang=%4


%mx% "seq=%txt_gen%" "proc='d3d5d6<80 0>gen</80><3 0>',replace(v3,' ',''),'</3>'" create=%db% now -all
%mx% "seq=%txt_gen%" "proc='d*<80 0>lab</80><1 0>',v1,'</1><2 0>',v5,'</2><3 0>',v6,'</3><4 0>',v7,'</4>'" append=db% now -all
%mx% "seq=%txt_lang%" "proc='d*<80 0>hlp</80><1 0>',v1,'</1><2 0>',v3,'</2><3 0>',v4,'</3><4 0>',v5,'</4>'" append=%db% now -all

echo 1 0 v1 > %db%.fst
echo 2 0 v80 >> %db%.fst
echo 3 0 v1,v80 >> %db%.fst

%mx% %db% "fst=@" fullinv=%db%