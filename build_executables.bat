@echo off
REM メール一括送信ツール - 実行ファイルビルドスクリプト（Windows版）

echo === メール一括送信ツール ビルドスクリプト ===
echo.

REM 必要なパッケージの確認とインストール
echo 必要なパッケージを確認中...
pip list | findstr /C:"pyinstaller" >nul
if errorlevel 1 (
    echo PyInstallerがインストールされていません。インストールします...
    pip install pyinstaller
)

pip list | findstr /C:"customtkinter" >nul
if errorlevel 1 (
    echo CustomTkinterがインストールされていません。インストールします...
    pip install customtkinter
)

pip list | findstr /C:"chardet" >nul
if errorlevel 1 (
    echo chardetがインストールされていません。インストールします...
    pip install chardet
)

echo.
echo ビルドを開始します...
echo.

REM 既存のビルドファイルをクリーンアップ
if exist build (
    echo 既存のbuildディレクトリを削除中...
    rmdir /s /q build
)

if exist dist (
    echo 既存のdistディレクトリを削除中...
    rmdir /s /q dist
)

if exist EmailBulkSender.spec (
    del EmailBulkSender.spec
)

if exist GmailBulkSender.spec (
    del GmailBulkSender.spec
)

echo.
echo 1/2: EmailBulkSender（汎用版）をビルド中...
pyinstaller --onefile --windowed --name="EmailBulkSender" email_bulk_sender_gui.py

if errorlevel 1 (
    echo × EmailBulkSenderのビルドに失敗しました
    pause
    exit /b 1
)
echo ✓ EmailBulkSenderのビルドが完了しました

echo.
echo 2/2: GmailBulkSender（Gmail専用版）をビルド中...
pyinstaller --onefile --windowed --name="GmailBulkSender" gmail_bulk_sender_gui.py

if errorlevel 1 (
    echo × GmailBulkSenderのビルドに失敗しました
    pause
    exit /b 1
)
echo ✓ GmailBulkSenderのビルドが完了しました

echo.
echo === ビルド完了 ===
echo.
echo 実行ファイルは dist\ ディレクトリに作成されました:
dir dist\*.exe
echo.
echo Windows用の実行ファイル（.exe）が作成されました。
echo ダブルクリックで起動できます。
echo.
pause
