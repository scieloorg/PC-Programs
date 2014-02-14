cisis\mx %1\title\title     text=%2 "proc=if v68='%2'  then else 'd*' fi" append=temp\serial\title\title now -all
cisis\mx %1\issue\issue     "proc=if s(mpl,v930,mpu)=s(mpl,'%2',mpu) then else 'd*' fi" append=temp\serial\issue\issue now -all
cisis\mx %1\section\section "proc=if s(mpl,v930,mpu)=s(mpl,'%2',mpu) then else 'd*' fi" append=temp\serial\section\section now -all

cisis\mx temp\serial\title\title now +control
cisis\mx temp\serial\issue\issue now +control
cisis\mx temp\serial\section\section now +control
