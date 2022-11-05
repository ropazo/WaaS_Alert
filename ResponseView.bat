# Visualizador de archivos .response
# Usar el explorador de archivos para registrar la aplicación asociada a .presponse

# Para registrar un ícono asociados a los archivos:
# https://www.winhelponline.com/blog/change-default-icon-file-type-windows/

echo off
cls
title %~n1
mode con: cols=110 lines=50

python "C:\git\WaaS_Alert\ResponseView.py" %1
set /p DUMMY=ENTER para salir...
