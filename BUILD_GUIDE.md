# スタンドアロン実行ファイル作成ガイド

このガイドでは、メール一括送信ツールをスタンドアロン実行ファイル（Windows: .exe、Linux/Mac: バイナリ）に変換する方法を説明します。

## 必要な環境

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## ビルド方法

### 自動ビルド（推奨）

#### Windows
1. コマンドプロンプトまたはPowerShellを開く
2. プロジェクトディレクトリに移動
3. 以下のコマンドを実行:
   ```cmd
   build_executables.bat
   ```

#### Linux/Mac
1. ターミナルを開く
2. プロジェクトディレクトリに移動
3. 実行権限を付与:
   ```bash
   chmod +x build_executables.sh
   ```
4. ビルドスクリプトを実行:
   ```bash
   ./build_executables.sh
   ```

### 手動ビルド

#### 1. 必要なパッケージのインストール

```bash
pip install pyinstaller customtkinter chardet
```

#### 2. 汎用版（email_bulk_sender_gui）のビルド

```bash
pyinstaller --onefile --windowed --name="EmailBulkSender" email_bulk_sender_gui.py
```

#### 3. Gmail専用版（gmail_bulk_sender_gui）のビルド

```bash
pyinstaller --onefile --windowed --name="GmailBulkSender" gmail_bulk_sender_gui.py
```

## ビルドオプションの説明

- `--onefile`: 単一の実行ファイルを作成（すべての依存関係を含む）
- `--windowed`: コンソールウィンドウを表示しない（GUIアプリ用）
- `--name`: 実行ファイルの名前を指定

## 追加オプション（必要に応じて）

### アイコンを追加する

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="EmailBulkSender" email_bulk_sender_gui.py
```

### ファイルサイズを削減する

```bash
pyinstaller --onefile --windowed --name="EmailBulkSender" --exclude-module matplotlib --exclude-module numpy email_bulk_sender_gui.py
```

## 出力ファイル

ビルドが完了すると、以下のディレクトリに実行ファイルが作成されます:

```
dist/
├── EmailBulkSender       # 汎用版（Windows: EmailBulkSender.exe）
└── GmailBulkSender       # Gmail専用版（Windows: GmailBulkSender.exe）
```

## 実行ファイルの配布

### Windows
- `dist/EmailBulkSender.exe`
- `dist/GmailBulkSender.exe`

これらのファイルを配布するだけで、Pythonがインストールされていない環境でも実行できます。

### 注意事項
- Windows用の.exeファイルを作成するには、Windows環境でビルドする必要があります
- Linux用のバイナリを作成するには、Linux環境でビルドする必要があります
- Mac用のバイナリを作成するには、Mac環境でビルドする必要があります

## トラブルシューティング

### ビルドエラーが発生する場合

1. PyInstallerを最新版に更新:
   ```bash
   pip install --upgrade pyinstaller
   ```

2. キャッシュをクリア:
   ```bash
   pip cache purge
   ```

3. 仮想環境を使用する:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install pyinstaller customtkinter chardet
   ```

### 実行ファイルが起動しない場合

1. `--windowed` オプションを外して再ビルド（エラーメッセージが表示されます）:
   ```bash
   pyinstaller --onefile --name="EmailBulkSender" email_bulk_sender_gui.py
   ```

2. ログファイルを確認:
   - ビルドログ: `build/EmailBulkSender/warn-EmailBulkSender.txt`

### ファイルサイズが大きい場合

デフォルトでは、すべての依存関係が含まれるため、ファイルサイズが大きくなります（50-100MB程度）。これは正常です。

必要に応じて、不要なモジュールを除外することでサイズを削減できます:

```bash
pyinstaller --onefile --windowed \
  --exclude-module matplotlib \
  --exclude-module numpy \
  --exclude-module scipy \
  --name="EmailBulkSender" \
  email_bulk_sender_gui.py
```

## クロスプラットフォーム対応

Windows、Linux、Macの3つのプラットフォームで実行ファイルを作成する場合:

1. 各プラットフォームで個別にビルドする
2. GitHub ActionsやCI/CDツールを使用して自動ビルドする
3. PyInstallerの仮想環境を使用する（高度）

## 参考リンク

- [PyInstaller公式ドキュメント](https://pyinstaller.org/)
- [CustomTkinter公式ドキュメント](https://customtkinter.tomschimansky.com/)
