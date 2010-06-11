copy %1\title\tit_issn.fst temp\serial\title\
copy %1\section\section.fst temp\serial\section\
copy %1\issue\issue.fst temp\serial\issue\

cisis\mx temp\serial\title\title fst=@%1\title\tit_issn.fst fullinv=temp\serial\title\tit_issn 
cisis\mx temp\serial\section\section fst=@%1\section\section.fst fullinv=temp\serial\section\section 
cisis\mx temp\serial\issue\issue fst=@%1\issue\issue.fst fullinv=temp\serial\issue\issue 
