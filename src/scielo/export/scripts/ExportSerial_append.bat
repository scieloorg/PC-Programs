cisis\mx %1\title\title     text=%2 "proc=if v68='%2'  then else 'd*' fi" append=temp\serial\title\title now -all
cisis\mx %1\issue\issue     "proc=if s(mpu,v930,mpl)=s(mpu,'%2',mpl) then else 'd*' fi" append=temp\serial\issue\issue now -all
cisis\mx %1\section\section "proc=if s(mpu,v930,mpl)=s(mpu,'%2',mpl) then else 'd*' fi" append=temp\serial\section\section now -all

cisis\mx temp\serial\title\title now +control
cisis\mx temp\serial\issue\issue now +control
cisis\mx temp\serial\section\section now +control
