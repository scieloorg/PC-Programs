

%2 "seq=%1," lw=9999 "pft=if instr(v1,'=')>0 then 'set ',replace(mid(v1,1,instr(v1,'=')),' ','_'),mid(v1,instr(v1,'=')+1,size(v1)),/ fi" now >  temp\setParameters.bat

call temp\setParameters.bat


