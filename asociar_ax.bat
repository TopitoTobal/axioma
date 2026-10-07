@echo off
setlocal

set "EXE_PATH=%~dp0dist\axioma.exe"

if not exist "%EXE_PATH%" (
    echo ERROR: No se encuentra axioma.exe en %~dp0dist
    pause
    exit /b 1
)

echo Asociando .ax con Axioma...
assoc .ax=Axioma.File
ftype Axioma.File="%EXE_PATH%" "%1"

echo.
echo Hecho! Los archivos .ax ahora se abriran con Axioma.
echo Puedes probarlo haciendo doble clic en un archivo .ax
pause
