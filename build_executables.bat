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

if exist EmailBulkSender.spec (
    del EmailBulkSender.spec
)

if exist GmailBulkSender.spec (
    del GmailBulkSender.spec
)

echo.
echo 1/2: Building EmailBulkSender (Generic version)...
pyinstaller --onefile --windowed --name="EmailBulkSender" email_bulk_sender_gui.py

if errorlevel 1 (
    echo [FAILED] EmailBulkSender build failed
    pause
    exit /b 1
)
echo [SUCCESS] EmailBulkSender build completed

echo.
echo 2/2: Building GmailBulkSender (Gmail version)...
pyinstaller --onefile --windowed --name="GmailBulkSender" gmail_bulk_sender_gui.py

if errorlevel 1 (
    echo [FAILED] GmailBulkSender build failed
    pause
    exit /b 1
)
echo [SUCCESS] GmailBulkSender build completed

echo.
echo === Build Complete ===
echo.
echo Executables created in dist\ directory:
dir dist\*.exe
echo.
echo Windows executable files (.exe) have been created.
echo You can run them by double-clicking.
echo.
pause
