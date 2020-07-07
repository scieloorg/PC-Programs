set apppath=%1
set python_call=%2

cd %apppath%\bin\xml
%python_call% download_markup_journals.py