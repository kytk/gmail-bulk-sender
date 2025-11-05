#!/bin/bash
# メール一括送信ツール - 実行ファイルビルドスクリプト

echo "=== メール一括送信ツール ビルドスクリプト ==="
echo ""

# 必要なパッケージの確認
echo "必要なパッケージを確認中..."
pip list | grep -q pyinstaller
if [ $? -ne 0 ]; then
    echo "PyInstallerがインストールされていません。インストールしますか？ (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        pip install pyinstaller
    else
        echo "PyInstallerが必要です。終了します。"
        exit 1
    fi
fi

pip list | grep -q customtkinter
if [ $? -ne 0 ]; then
    echo "CustomTkinterがインストールされていません。インストールしますか？ (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        pip install customtkinter
    else
        echo "CustomTkinterが必要です。終了します。"
        exit 1
    fi
fi

pip list | grep -q chardet
if [ $? -ne 0 ]; then
    echo "chardetがインストールされていません。インストールしますか？ (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        pip install chardet
    else
        echo "chardetが必要です。終了します。"
        exit 1
    fi
fi

echo ""
echo "ビルドを開始します..."
echo ""

# 既存のビルドファイルをクリーンアップ
if [ -d "build" ]; then
    echo "既存のbuildディレクトリを削除中..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "既存のdistディレクトリを削除中..."
    rm -rf dist
fi

if [ -f "EmailBulkSender.spec" ]; then
    rm EmailBulkSender.spec
fi

if [ -f "GmailBulkSender.spec" ]; then
    rm GmailBulkSender.spec
fi

echo ""
echo "1/2: EmailBulkSender（汎用版）をビルド中..."
pyinstaller --onefile --windowed --name="EmailBulkSender" email_bulk_sender_gui.py

if [ $? -eq 0 ]; then
    echo "✓ EmailBulkSenderのビルドが完了しました"
else
    echo "✗ EmailBulkSenderのビルドに失敗しました"
    exit 1
fi

echo ""
echo "2/2: GmailBulkSender（Gmail専用版）をビルド中..."
pyinstaller --onefile --windowed --name="GmailBulkSender" gmail_bulk_sender_gui.py

if [ $? -eq 0 ]; then
    echo "✓ GmailBulkSenderのビルドが完了しました"
else
    echo "✗ GmailBulkSenderのビルドに失敗しました"
    exit 1
fi

echo ""
echo "=== ビルド完了 ==="
echo ""
echo "実行ファイルは dist/ ディレクトリに作成されました:"
ls -lh dist/
echo ""
echo "注意: Linux環境でビルドした場合、実行ファイルはLinux用です。"
echo "      Windows用の.exeファイルを作成するには、Windows環境でこのスクリプトを実行してください。"
echo ""
