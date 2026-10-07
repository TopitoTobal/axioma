@echo off
setlocal

:: Auto-elevar a administrador si no lo es
fltmc >nul 2>&1 || (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~s0'"
    exit /b
)

set "DIST_DIR=%~dp0dist"
set "EXE_PATH=%DIST_DIR%\axioma.exe"

if not exist "%EXE_PATH%" (
    echo ERROR: No se encuentra axioma.exe en %DIST_DIR%
    echo Ejecuta primero: pyinstaller --onefile --name=axioma --distpath=dist --clean --noconfirm --console run.py
    pause
    exit /b 1
)

echo Agregando %DIST_DIR% al PATH del usuario...
setx PATH "%DIST_DIR%;%PATH%"

echo Asociando archivos .ax con Axioma...
assoc .ax=Axioma.File
ftype Axioma.File="%EXE_PATH%" "%1"

echo.
echo Instalacion completada!
echo Ahora puedes usar 'axioma' desde cualquier terminal.
echo.
echo Ejemplos:
echo   axioma archivo.ax
echo   axioma             (abre REPL interactivo)
echo.
echo NOTA: Reinicia la terminal para que los cambios surtan efecto.
pause
