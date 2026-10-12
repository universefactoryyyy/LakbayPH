@echo off
REM build.bat - makes dist\LakbayPH.exe (one file, no console window)
cd /d "%~dp0"

echo [1/3] Checking Pillow and PyInstaller...
python -m pip install pillow pyinstaller
if errorlevel 1 goto failed

echo [2/3] Running the tests...
python test_lakbayph.py
if errorlevel 1 goto failed

echo [3/3] Building LakbayPH.exe...
REM --add-data bundles the assets folder (logo, placeholder, default pictures, seed_data.sql)
python -m PyInstaller --noconfirm --clean --onefile --windowed --name LakbayPH --icon "assets\logo.ico" --add-data "assets;assets" main.py
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
