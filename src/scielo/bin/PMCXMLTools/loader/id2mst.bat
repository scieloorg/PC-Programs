set cisis_path=%1
set idfile=%2
set db=%3
%cisis_path%\id2i %idfile% create=temp
%cisis_path%\mx temp now -all append=%db%

