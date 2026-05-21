@echo off
setlocal

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
