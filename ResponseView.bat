echo off
cls
title %~n1
mode con: cols=100 lines=50

python "C:\git\WaaS_Alert\ResponseView.py" %1
set /p DUMMY=ENTER para salir...
