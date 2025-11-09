@echo off
REM Email Bulk Sender Tool - Build Script for Windows

echo === Email Bulk Sender Build Script ===
echo.

REM Check and install required packages
echo Checking required packages...
pip list | findstr /C:"pyinstaller" >nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing...
    pip install pyinstaller
)

pip list | findstr /C:"customtkinter" >nul
if errorlevel 1 (
    echo CustomTkinter is not installed. Installing...
    pip install customtkinter
)

pip list | findstr /C:"chardet" >nul
if errorlevel 1 (
    echo chardet is not installed. Installing...
    pip install chardet
)

echo.
echo Starting build process...
echo.

REM Clean up existing build files
if exist build (
    echo Removing existing build directory...
    rmdir /s /q build
)

if exist dist (
    echo Removing existing dist directory...
    rmdir /s /q dist
)

if exist EmailBulkSender_win.spec (
    del EmailBulkSender_win.spec
)

if exist GmailBulkSender_win.spec (
    del GmailBulkSender_win.spec
)

echo.
echo 1/2: Building EmailBulkSender_win (Generic version)...
pyinstaller --onefile --windowed --name="EmailBulkSender_win" email_bulk_sender_gui.py

if errorlevel 1 (
    echo [FAILED] EmailBulkSender_win build failed
    pause
    exit /b 1
)
echo [SUCCESS] EmailBulkSender_win build completed

echo.
echo 2/2: Building GmailBulkSender_win (Gmail version)...
pyinstaller --onefile --windowed --name="GmailBulkSender_win" gmail_bulk_sender_gui.py

if errorlevel 1 (
    echo [FAILED] GmailBulkSender_win build failed
    pause
    exit /b 1
)
echo [SUCCESS] GmailBulkSender_win build completed

echo.
echo === Build Complete ===
echo.
echo Executables created in dist\ directory:
dir dist\*.exe
echo.

REM Create distribution packages with samples
echo.
echo Creating distribution packages...
echo.

REM Create temporary directories for packaging
mkdir dist\EmailBulkSender_win_package 2>nul
mkdir dist\GmailBulkSender_win_package 2>nul

REM Copy files for EmailBulkSender package
copy dist\EmailBulkSender_win.exe dist\EmailBulkSender_win_package\
xcopy examples dist\EmailBulkSender_win_package\examples\ /E /I /Y
copy README.md dist\EmailBulkSender_win_package\
copy LICENSE dist\EmailBulkSender_win_package\

REM Copy files for GmailBulkSender package
copy dist\GmailBulkSender_win.exe dist\GmailBulkSender_win_package\
xcopy examples dist\GmailBulkSender_win_package\examples\ /E /I /Y
copy README.md dist\GmailBulkSender_win_package\
copy LICENSE dist\GmailBulkSender_win_package\

REM Create zip files (using PowerShell)
echo Creating EmailBulkSender_win.zip...
powershell -command "Compress-Archive -Path dist\EmailBulkSender_win_package\* -DestinationPath dist\EmailBulkSender_win.zip -Force"

echo Creating GmailBulkSender_win.zip...
powershell -command "Compress-Archive -Path dist\GmailBulkSender_win_package\* -DestinationPath dist\GmailBulkSender_win.zip -Force"

REM Clean up temporary directories
rmdir /s /q dist\EmailBulkSender_win_package
rmdir /s /q dist\GmailBulkSender_win_package

echo.
echo === Packaging Complete ===
echo.
echo Created distribution packages:
dir dist\*.zip
echo.
echo Package contents:
echo - Executable file (.exe)
echo - Sample files (examples/)
echo - README.md
echo - LICENSE
echo.
echo Windows executable files (.exe) and distribution packages (.zip) have been created.
echo You can distribute the .zip files to users without Python.
echo.
pause
