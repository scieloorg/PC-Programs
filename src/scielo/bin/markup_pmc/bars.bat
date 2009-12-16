MX=C:\home\scielo\www\proc\cisis1030\mx

%MX% "seq=%1" create=d:\temp\x now -all

%MX% d:\temp\x lw=99999 "pft=if a(v1) then # else if instr(v1,'down')=0 then v1,'|' fi, fi" now > d:\temp\x2

%MX% seq=d:\temp\x2 create=d:\temp\x2 now -all


%MX% seq=d:\temp\x2 "proc='d9001a9001{',mid(v1,1,instr(v1,';')),,'{'" "proc='d1d2d3d4d5d6d7d8d9d10d11d12d13d14d15d16d17d18d19d20',if p(v2) then 'a2{',v9001,v2,,'{', fi,,if p(v3) then 'a2{',v9001,v3,'{', fi,,if p(v4) then 'a2{',v9001,v4,'{', fi,,if p(v5) then 'a2{',v9001,v5,'{', fi,,if p(v6) then 'a2{',v9001,v6,'{', fi,,if p(v7) then 'a2{',v9001,v7,'{', fi,,if p(v8) then 'a2{',v9001,v8,'{', fi,,if p(v9) then 'a2{',v9001,v9,'{',fi,if p(v10) then 'a2{',v9001,v10,'{', fi,,,if p(v11) then 'a2{',v9001,v11,'{', fi,,if p(v12) then 'a2{',v9001,v12,'{', fi,,if p(v13) then 'a2{',v9001,v13,'{', fi,,if p(v14) then 'a2{',v9001,v14,'{', fi,,if p(v15) then 'a2{'v9001,v15,,'{', fi,,if p(v16) then 'a2{',v9001,v16,,'{', fi,,if p(v17) then 'a2{',v9001,v17,'{', fi,,if p(v18) then 'a2{',v9001,v18,'{', fi,,if p(v19) then 'a2{',v9001,v19,,'{', fi,,if p(v20) then 'a2{',v9001,v20,,'{', fi,,,if p(v21) then 'a2{',v9001,v21,,'{', fi," create=d:\temp\x3 now -all

%MX% d:\temp\x3 lw=99999 "pft=(v2/)" now > d:\temp\x3.txt

%MX% "seq=d:\temp\x3.txt;" lw=9999 "pft=if v2<>'down' then v1,';',v2,#,v3,#,# fi" now > %1.txt


notepad %1.txt


