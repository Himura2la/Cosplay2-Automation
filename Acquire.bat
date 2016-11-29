@echo off

set pythonpath=%APPDATA%\..\Local\Programs\Python\Python35-32\python.exe
rem pythonpath="%PROGRAMFILES(X86)%\Python35-32\python.exe"

%pythonpath% acquire.py
%pythonpath% make_db.py
pause