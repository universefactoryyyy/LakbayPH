@echo off
REM build.bat - makes dist\LakbayPH.exe (one file, no console window)
cd /d "%~dp0"

REM Use the "py" launcher if it is installed, otherwise "python"
set PY=python
py --version >nul 2>nul
if not errorlevel 1 set PY=py

echo [1/3] Checking Pillow and PyInstaller...
%PY% -m pip install pillow pyinstaller
if errorlevel 1 goto failed

echo [2/3] Running the tests...
%PY% test_lakbayph.py
if errorlevel 1 goto failed

echo [3/3] Building LakbayPH.exe...
REM --add-data bundles the assets folder (logo, placeholder, default pictures, seed_data.sql)
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name LakbayPH --icon "assets\logo.ico" --add-data "assets;assets" main.py
if errorlevel 1 goto failed

echo.
echo Done! The app is in dist\LakbayPH.exe
pause
exit /b 0

:failed
echo.
echo The build failed. Read the messages above.
pause
exit /b 1
