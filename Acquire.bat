@echo off

set pythonpath=%APPDATA%\..\Local\Programs\Python\Python35-32\python.exe
rem set pythonpath="%PROGRAMFILES(X86)%\Python35-32\python.exe"

%pythonpath% get_data.py
pause