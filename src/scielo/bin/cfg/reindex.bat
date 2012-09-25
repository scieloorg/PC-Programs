set serial=%1\serial


if "@%serial%" == "@\serial" goto ERROR1
if not exist %serial% goto ERROR2


if exist %serial%\section\section.mst mx %serial%\section\section fst=@ fullinv=%serial%\section\section
if exist %serial%\issue\issue.mst     mx %serial%\issue\issue     fst=@ fullinv=%serial%\issue\issue
if exist %serial%\code\code.mst       mx %serial%\code\code       fst=@ fullinv=%serial%\code\code
if exist %serial%\code\newcode.mst    mx %serial%\code\newcode    fst=@ fullinv=%serial%\code\newcode
if exist %serial%\title\title.mst     mx %serial%\title\title     fst=@%serial%\title\tit_issn.fst fullinv=%serial%\title\tit_issn



:ERROR1
echo execute 
echo reindex c:\scielo
goto FIM

:ERROR2
echo Invalid path %serial%
:FIM
