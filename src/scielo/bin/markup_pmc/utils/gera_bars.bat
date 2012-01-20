MX=%1
PT_BARS=%2
TR=%3
WORK=%4
TR_PT=%5
TR_EN=%6
TR_ES=%7

DB=%WORK%/PT_BARS
%MX% "seq=%PT_BARS%;" create=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) then if ref(mfn-1,v1)='' then 'a900{',v1,'{a901{parent{'  fi fi" copy=%DB% now -all
 
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all
%MX% %DB% lw=9999 "proc=if p(v1) and ref(mfn-1,v900)<>'' then 'a900{',ref(mfn-1,v900),'{a901{child{'  fi fi" copy=%DB% now -all

%MX% %DB% lw=999 "pft=if v1<>'down' and v901<>'parent' then v900,';',v1,'|',v2,# fi" now 