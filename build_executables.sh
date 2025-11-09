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

# プラットフォームとアーキテクチャの検出
OS_TYPE=$(uname -s)
ARCH=$(uname -m)

if [ "$OS_TYPE" = "Linux" ]; then
    SUFFIX="_lnx"
    PLATFORM_NAME="Linux"
elif [ "$OS_TYPE" = "Darwin" ]; then
    if [ "$ARCH" = "arm64" ]; then
        SUFFIX="_mac_arm64"
        PLATFORM_NAME="macOS (ARM64)"
    elif [ "$ARCH" = "x86_64" ]; then
        SUFFIX="_mac_amd64"
        PLATFORM_NAME="macOS (AMD64)"
    else
        SUFFIX="_mac_${ARCH}"
        PLATFORM_NAME="macOS (${ARCH})"
    fi
else
    SUFFIX="_${OS_TYPE}"
    PLATFORM_NAME="${OS_TYPE}"
fi

echo "検出されたプラットフォーム: ${PLATFORM_NAME}"
echo ""

if [ -f "EmailBulkSender${SUFFIX}.spec" ]; then
    rm "EmailBulkSender${SUFFIX}.spec"
fi

if [ -f "GmailBulkSender${SUFFIX}.spec" ]; then
    rm "GmailBulkSender${SUFFIX}.spec"
fi

echo ""
echo "1/2: EmailBulkSender${SUFFIX}（汎用版）をビルド中..."
pyinstaller --onefile --windowed --name="EmailBulkSender${SUFFIX}" email_bulk_sender_gui.py

if [ $? -eq 0 ]; then
    echo "✓ EmailBulkSender${SUFFIX}のビルドが完了しました"
else
    echo "✗ EmailBulkSender${SUFFIX}のビルドに失敗しました"
    exit 1
fi

echo ""
echo "2/2: GmailBulkSender${SUFFIX}（Gmail専用版）をビルド中..."
pyinstaller --onefile --windowed --name="GmailBulkSender${SUFFIX}" gmail_bulk_sender_gui.py

if [ $? -eq 0 ]; then
    echo "✓ GmailBulkSender${SUFFIX}のビルドが完了しました"
else
    echo "✗ GmailBulkSender${SUFFIX}のビルドに失敗しました"
    exit 1
fi

echo ""
echo "=== ビルド完了 ==="
echo ""
echo "実行ファイルは dist/ ディレクトリに作成されました:"
ls -lh dist/
echo ""

# Create distribution packages with samples
echo ""
echo "配布パッケージを作成中..."
echo ""

# Create temporary directories for packaging
mkdir -p "dist/EmailBulkSender${SUFFIX}_package"
mkdir -p "dist/GmailBulkSender${SUFFIX}_package"

# Copy files for EmailBulkSender package
cp "dist/EmailBulkSender${SUFFIX}" "dist/EmailBulkSender${SUFFIX}_package/"
cp -r examples "dist/EmailBulkSender${SUFFIX}_package/"
cp README.md "dist/EmailBulkSender${SUFFIX}_package/"
cp LICENSE "dist/EmailBulkSender${SUFFIX}_package/"

# Copy files for GmailBulkSender package
cp "dist/GmailBulkSender${SUFFIX}" "dist/GmailBulkSender${SUFFIX}_package/"
cp -r examples "dist/GmailBulkSender${SUFFIX}_package/"
cp README.md "dist/GmailBulkSender${SUFFIX}_package/"
cp LICENSE "dist/GmailBulkSender${SUFFIX}_package/"

# Create zip files
echo "Creating EmailBulkSender${SUFFIX}.zip..."
cd "dist/EmailBulkSender${SUFFIX}_package"
zip -r "../EmailBulkSender${SUFFIX}.zip" .
cd ../..

echo "Creating GmailBulkSender${SUFFIX}.zip..."
cd "dist/GmailBulkSender${SUFFIX}_package"
zip -r "../GmailBulkSender${SUFFIX}.zip" .
cd ../..

# Clean up temporary directories
rm -rf "dist/EmailBulkSender${SUFFIX}_package"
rm -rf "dist/GmailBulkSender${SUFFIX}_package"

echo ""
echo "=== パッケージング完了 ==="
echo ""
echo "作成された配布パッケージ:"
ls -lh dist/*.zip
echo ""
echo "プラットフォーム: ${PLATFORM_NAME}"
echo "作成されたファイル:"
echo "  - EmailBulkSender${SUFFIX}"
echo "  - EmailBulkSender${SUFFIX}.zip"
echo "  - GmailBulkSender${SUFFIX}"
echo "  - GmailBulkSender${SUFFIX}.zip"
echo ""
echo "パッケージ内容:"
echo "  - 実行ファイル"
echo "  - サンプルファイル (examples/)"
echo "  - README.md"
echo "  - LICENSE"
echo ""
echo "注意: 各プラットフォーム専用の実行ファイルです。"
echo "      他のプラットフォーム用のファイルを作成するには、そのプラットフォームでビルドしてください。"
echo "      .zipファイルをPythonがインストールされていないユーザーに配布できます。"
echo ""
