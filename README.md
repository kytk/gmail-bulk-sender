# Gmail一斉送信ツール

Gmailを使用して、CSVリストに基づいた個別対応のメールを一斉送信するPythonスクリプトです。

## 目次

- [機能](#機能)
- [必要な環境](#必要な環境)
- [セットアップ](#セットアップ)
- [ファイルの準備](#ファイルの準備)
- [使い方](#使い方)
- [トラブルシューティング](#トラブルシューティング)
- [注意事項](#注意事項)
- [よくある質問](#よくある質問)

## 機能

- CSVファイルから受信者リストを読み込み
- テンプレート内の`{氏名}`を各受信者の名前に自動置換
- 件名と本文を1つのテンプレートファイルで管理
- CC、BCC、Reply-To の設定に対応
- Gmail SMTP経由で安全に送信
- 送信制限対策（送信間隔の自動調整）
- 送信結果のリアルタイム表示

## 必要な環境

- Python 3.6以上
- Gmailアカウント（2段階認証が有効であること）
- インターネット接続

### 必要なPythonライブラリ

標準ライブラリのみ使用するため、追加インストールは不要です。

## セットアップ

### 1. スクリプトのダウンロード

```bash
# リポジトリをクローン、またはファイルをダウンロード
git clone https://github.com/kytk/gmail-bulk-sender.git
cd gmail-bulk-sender

# または、bulk_email_sender.py を直接ダウンロード
```

### 2. Gmailアプリパスワードの取得

**重要**: 通常のGmailパスワードではなく、「アプリパスワード」を使用する必要があります。

#### 手順：

1. **Googleアカウントにアクセス**
   - [https://myaccount.google.com/](https://myaccount.google.com/) にアクセス
   - Gmailアカウントでログイン

2. **2段階認証を有効化**（まだの場合）
   - 左メニューから「セキュリティ」を選択
   - 「Google へのログイン」セクションで「2段階認証プロセス」をクリック
   - 画面の指示に従って設定

3. **アプリパスワードを生成**
   - 「セキュリティ」ページに戻る
   - 上の検索窓に「アプリ パスワード」と入力
   - 「アプリ固有のパスワードを新規作成するには、下にアプリ名を入力してください」に任意のアプリ名を入力（例：「一斉送信メール」）
   - 「作成」をクリック

4. **パスワードをコピー**
   - 表示された16文字のパスワードをコピー
   - **このパスワードは再表示されないため、安全な場所に保存してください**

   例：`abcd efgh ijkl mnop`（スペースは入力時に不要）

### 3. ファイル構成の確認

プロジェクトフォルダに以下のファイルを配置します：

```
gmail-bulk-sender/
├── bulk_email_sender.py  # メインスクリプト
├── list.csv              # 受信者リスト
├── body.txt              # メールテンプレート
└── README.md             # このファイル
```

## ファイルの準備

### list.csv（受信者リスト）

CSVファイルに受信者の情報を記載します。

**フォーマット：**
```csv
氏名,メールアドレス
山田太郎,yamada@example.com
佐藤花子,sato@example.com
鈴木一郎,suzuki@example.com
田中美咲,tanaka@example.com
```

**注意点：**
- 1行目は必ずヘッダー行（`氏名,メールアドレス`）
- 文字コードは UTF-8 で保存
- Excelで編集する場合、保存時に「CSV UTF-8（コンマ区切り）」を選択

### body.txt（メールテンプレート）

メールの件名と本文を記載します。

**フォーマット：**
```
【重要】新サービスのご案内 - {氏名}様

{氏名}様

いつもお世話になっております。
株式会社サンプルの営業部です。

この度、新サービス「○○○」をリリースいたしましたので、
ご案内させていただきます。

■ サービス概要
- 特徴1：○○○
- 特徴2：△△△
- 特徴3：□□□

詳細につきましては、下記URLをご参照ください。
https://example.com/service

ご不明な点がございましたら、お気軽にお問い合わせください。

今後とも何卒よろしくお願い申し上げます。

────────────────────────
株式会社サンプル
営業部 山田太郎
Email: info@example.com
Tel: 03-1234-5678
────────────────────────
```

**ルール：**
- **1行目**: 件名（`{氏名}`で受信者名を挿入可能）
- **2行目**: 空行（必須）
- **3行目以降**: 本文（`{氏名}`で受信者名を挿入可能）

## 使い方

### 1. スクリプトの実行

```bash
python bulk_email_sender.py
```

### 2. 対話形式での入力

実行すると以下の項目を順番に入力します：

```
=== Gmail一斉送信ツール ===

送信元Gmailアドレス: your.email@gmail.com
Gmailアプリパスワード: ****************
受信者リストCSVファイル (デフォルト: list.csv): 
メールテンプレートファイル (デフォルト: body.txt): 
CC (複数の場合はカンマ区切り、不要ならEnter): cc@example.com
BCC (複数の場合はカンマ区切り、不要ならEnter): 
Reply-To (不要ならEnter): reply@example.com
```

**入力のポイント：**
- **Gmailアプリパスワード**: 取得した16文字のパスワード（スペースなしで入力）
- **ファイル名**: Enterキーで デフォルト値（list.csv、body.txt）を使用
- **CC/BCC**: 複数指定する場合は `email1@example.com,email2@example.com` のようにカンマ区切り
- **不要な項目**: そのままEnterキーを押す

### 3. 送信内容の確認

入力後、送信内容が表示されます：

```
=== 送信内容確認 ===
件名: 【重要】新サービスのご案内 - {氏名}様
送信先: 4件
送信元: your.email@gmail.com
CC: cc@example.com
Reply-To: reply@example.com

送信を開始しますか？ (yes/no): 
```

### 4. 送信開始

`yes` と入力すると送信が開始されます：

```
[1/4] 送信成功: 山田太郎 (yamada@example.com)
[2/4] 送信成功: 佐藤花子 (sato@example.com)
[3/4] 送信成功: 鈴木一郎 (suzuki@example.com)
[4/4] 送信成功: 田中美咲 (tanaka@example.com)

送信完了: 成功 4件, 失敗 0件
```

## トラブルシューティング

### エラー: 認証失敗

```
SMTP接続エラー: (535, b'5.7.8 Username and Password not accepted...')
```

**原因と対処法：**
1. アプリパスワードが間違っている → 再度確認・再生成
2. 2段階認証が無効 → Googleアカウントで有効化
3. 通常のパスワードを使用している → アプリパスワードを使用

### エラー: ファイルが見つからない

```
FileNotFoundError: [Errno 2] No such file or directory: 'list.csv'
```

**対処法：**
- ファイル名とパスを確認
- スクリプトと同じフォルダにファイルがあるか確認
- ファイル名の大文字小文字を確認

### エラー: 送信制限

```
SMTPDataError: (550, b'5.4.5 Daily sending quota exceeded')
```

**対処法：**
- Gmail無料版: 1日500通まで
- Google Workspace: 1日2,000通まで
- 翌日まで待つか、複数のアカウントで分散送信

### 文字化け

**対処法：**
- CSVファイルをUTF-8で保存
- body.txtをUTF-8で保存
- Windowsの場合、メモ帳で開いて「UTF-8」を選択して保存

## 注意事項

### 送信制限

- **無料Gmail**: 1日あたり500通まで
- **Google Workspace**: 1日あたり2,000通まで
- 1時間あたりの制限もあるため、大量送信時は注意

### セキュリティ

- アプリパスワードをコードに直接書かない
- アプリパスワードをGitにコミットしない
- 使用後は安全に保管
- 不要になったアプリパスワードは削除

### ベストプラクティス

1. **テスト送信**: 本番前に自分宛てにテスト送信
2. **少数から開始**: 最初は5-10件程度で動作確認
3. **送信リストの確認**: 送信前に必ず内容を確認
4. **エラーログ**: 失敗した送信先は記録して再送
5. **配信停止対応**: オプトアウトのリンクを含める

### 法的注意事項

- 受信者の同意なく営業メールを送信しない
- 特定電子メール法を遵守
- オプトアウト（配信停止）の手段を提供
- 個人情報を適切に管理

## よくある質問

### Q: HTMLメールを送信できますか？

A: 現在のバージョンはテキストメールのみ対応。HTMLメールを送りたい場合は、`MIMEText`の第2引数を`'html'`に変更し、body.txtにHTMLを記述してください。

### Q: 添付ファイルを送れますか？

A: 現在のバージョンは未対応。添付ファイル機能が必要な場合は、スクリプトの拡張が必要です。

### Q: 送信間隔を変更できますか？

A: `send_bulk_emails`メソッドの`delay`パラメータ（デフォルト1秒）を変更できます。

### Q: 複数の変数（氏名以外）を使えますか？

A: CSVに列を追加し、スクリプトを修正すれば可能です。例えば`{会社名}`や`{役職}`なども使用できます。

## ライセンス

このスクリプトは自由に使用・改変できます。

## サポート

問題や質問がある場合は、Issueを作成してください。

---

**作成日**: 2025年9月  
**バージョン**: 1.0

---

# Gmail Bulk Sender Tool

A Python script for sending personalized bulk emails via Gmail based on a CSV recipient list.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [File Preparation](#file-preparation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Important Notes](#important-notes)
- [FAQ](#faq)

## Features

- Load recipient list from CSV file
- Automatically replace `{氏名}` (name) placeholders with individual recipient names
- Manage subject and body in a single template file
- Support for CC, BCC, and Reply-To
- Secure sending via Gmail SMTP
- Rate limiting protection (automatic sending interval adjustment)
- Real-time sending status display

## Requirements

- Python 3.6 or higher
- Gmail account with 2-Step Verification enabled
- Internet connection

### Required Python Libraries

Only standard libraries are used, so no additional installation is required.

## Setup

### 1. Download the Script

```bash
# Clone the repository or download the files
git clone <repository-url>
cd gmail-bulk-sender

# Or download bulk_email_sender.py directly
```

### 2. Obtain Gmail App Password

**Important**: You must use an "App Password", not your regular Gmail password.

#### Steps:

1. **Access Google Account**
   - Go to [https://myaccount.google.com/](https://myaccount.google.com/)
   - Sign in with your Gmail account

2. **Enable 2-Step Verification** (if not already enabled)
   - Select "Security" from the left menu
   - Click "2-Step Verification" under "Signing in to Google"
   - Follow the on-screen instructions

3. **Generate App Password**
   - Return to the "Security" page
   - Enter "App passwords" in the search bar at the top
   - In "To create a new app-specific password, enter the app name below", enter any app name (e.g., "Bulk Email Sender")
   - Click "Create"

4. **Copy the Password**
   - Copy the 16-character password displayed
   - **This password will not be shown again, so save it securely**

   Example: `abcd efgh ijkl mnop` (spaces are not needed when entering)

### 3. Verify File Structure

Place the following files in your project folder:

```
gmail-bulk-sender/
├── bulk_email_sender.py  # Main script
├── list.csv              # Recipient list
├── body.txt              # Email template
└── README.md             # This file
```

## File Preparation

### list.csv (Recipient List)

Enter recipient information in the CSV file.

**Format:**
```csv
氏名,メールアドレス
山田太郎,yamada@example.com
佐藤花子,sato@example.com
鈴木一郎,suzuki@example.com
田中美咲,tanaka@example.com
```

**Notes:**
- First line must be the header row (`氏名,メールアドレス`)
- Save with UTF-8 encoding
- If editing in Excel, select "CSV UTF-8 (Comma delimited)" when saving

### body.txt (Email Template)

Write the email subject and body.

**Format:**
```
[Important] New Service Announcement - {氏名}様

{氏名}様

Thank you for your continued support.
This is the Sales Department of Sample Corporation.

We are pleased to announce the release of our new service "XXX".

■ Service Overview
- Feature 1: XXX
- Feature 2: YYY
- Feature 3: ZZZ

For more details, please visit:
https://example.com/service

If you have any questions, please feel free to contact us.

We look forward to your continued support.

────────────────────────
Sample Corporation
Sales Department - Taro Yamada
Email: info@example.com
Tel: 03-1234-5678
────────────────────────
```

**Rules:**
- **Line 1**: Subject (can use `{氏名}` to insert recipient name)
- **Line 2**: Empty line (required)
- **Line 3 onwards**: Body (can use `{氏名}` to insert recipient name)

## Usage

### 1. Run the Script

```bash
python bulk_email_sender.py
```

### 2. Interactive Input

You will be prompted to enter the following information:

```
=== Gmail一斉送信ツール ===

送信元Gmailアドレス: your.email@gmail.com
Gmailアプリパスワード: ****************
受信者リストCSVファイル (デフォルト: list.csv): 
メールテンプレートファイル (デフォルト: body.txt): 
CC (複数の場合はカンマ区切り、不要ならEnter): cc@example.com
BCC (複数の場合はカンマ区切り、不要ならEnter): 
Reply-To (不要ならEnter): reply@example.com
```

**Input Tips:**
- **Gmail App Password**: Enter the 16-character password (without spaces)
- **File names**: Press Enter to use default values (list.csv, body.txt)
- **CC/BCC**: For multiple addresses, separate with commas like `email1@example.com,email2@example.com`
- **Optional fields**: Just press Enter to skip

### 3. Confirm Sending Details

After input, the sending details will be displayed:

```
=== 送信内容確認 ===
件名: 【重要】新サービスのご案内 - {氏名}様
送信先: 4件
送信元: your.email@gmail.com
CC: cc@example.com
Reply-To: reply@example.com

送信を開始しますか？ (yes/no): 
```

### 4. Start Sending

Type `yes` to begin sending:

```
[1/4] 送信成功: 山田太郎 (yamada@example.com)
[2/4] 送信成功: 佐藤花子 (sato@example.com)
[3/4] 送信成功: 鈴木一郎 (suzuki@example.com)
[4/4] 送信成功: 田中美咲 (tanaka@example.com)

送信完了: 成功 4件, 失敗 0件
```

## Troubleshooting

### Error: Authentication Failed

```
SMTP接続エラー: (535, b'5.7.8 Username and Password not accepted...')
```

**Causes and Solutions:**
1. Incorrect app password → Verify or regenerate
2. 2-Step Verification disabled → Enable in Google Account
3. Using regular password → Use app password instead

### Error: File Not Found

```
FileNotFoundError: [Errno 2] No such file or directory: 'list.csv'
```

**Solutions:**
- Verify file name and path
- Confirm file is in the same folder as the script
- Check case sensitivity of file name

### Error: Sending Limit Exceeded

```
SMTPDataError: (550, b'5.4.5 Daily sending quota exceeded')
```

**Solutions:**
- Free Gmail: 500 messages per day limit
- Google Workspace: 2,000 messages per day limit
- Wait until the next day or distribute across multiple accounts

### Character Encoding Issues

**Solutions:**
- Save CSV file as UTF-8
- Save body.txt as UTF-8
- On Windows, open in Notepad and select "UTF-8" when saving

## Important Notes

### Sending Limits

- **Free Gmail**: Up to 500 messages per day
- **Google Workspace**: Up to 2,000 messages per day
- Be cautious with hourly limits for large volumes

### Security

- Do not hardcode app passwords in the script
- Do not commit app passwords to Git
- Store securely after use
- Delete unused app passwords

### Best Practices

1. **Test Sending**: Send to yourself before production use
2. **Start Small**: Begin with 5-10 recipients to verify
3. **Verify List**: Always check content before sending
4. **Error Logging**: Record failed recipients for resending
5. **Unsubscribe Option**: Include opt-out links

### Legal Considerations

- Do not send marketing emails without consent
- Comply with anti-spam laws (e.g., CAN-SPAM Act)
- Provide unsubscribe mechanisms
- Properly manage personal information

## FAQ

### Q: Can I send HTML emails?

A: The current version only supports plain text. For HTML emails, change the second parameter of `MIMEText` to `'html'` and write HTML in body.txt.

### Q: Can I send attachments?

A: Not supported in the current version. Script extension is required for attachment functionality.

### Q: Can I change the sending interval?

A: Yes, modify the `delay` parameter (default 1 second) in the `send_bulk_emails` method.

### Q: Can I use multiple variables (besides name)?

A: Yes, add columns to the CSV and modify the script. For example, you can use `{会社名}` (company name) or `{役職}` (title).

## License

This script is free to use and modify.

## Support

For issues or questions, please create an Issue.

---

**Created**: 23 September 2025
**Version**: 1.0
```
