import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr
from email import encoders
import time
from getpass import getpass
import os
from urllib.parse import quote
import mimetypes

# ==================== 設定セクション ====================
# ここで送信元情報とSMTPサーバー設定をしてください

# SMTPサーバー（空文字列の場合は実行時に入力を求めます）
DEFAULT_SMTP_SERVER = ""  # 例: "smtp.example.com" or "smtp.gmail.com"

# SMTPポート番号（空文字列の場合は実行時に入力を求めます。デフォルト: 587）
DEFAULT_SMTP_PORT = ""  # 例: "587" (TLS), "465" (SSL), "25" (非暗号化)

# メールアドレス（空文字列の場合は実行時に入力を求めます）
DEFAULT_EMAIL_ADDRESS = ""  # 例: "your.email@example.com"

# メールパスワード（空文字列の場合は実行時に入力を求めます）
# セキュリティ上、ここには記載せず実行時に入力することを推奨
DEFAULT_EMAIL_PASSWORD = ""

# 送信元表示名（空文字列の場合はメールアドレスのみ表示）
SENDER_DISPLAY_NAME = ""  # 例: "株式会社サンプル 営業部"

# 受信者リストCSVファイル（空文字列の場合はデフォルト: list.csv）
DEFAULT_CSV_FILE = ""  # 例: "recipients.csv"

# メールテンプレートファイル（空文字列の場合はデフォルト: body.txt）
DEFAULT_TEMPLATE_FILE = ""  # 例: "email_template.txt"

# CC（Noneの場合は実行時に入力を求め、""の場合は不要としてスキップ）
DEFAULT_CC = None  # 例: "cc@example.com" または "" (不要な場合)

# BCC（Noneの場合は実行時に入力を求め、""の場合は不要としてスキップ）
DEFAULT_BCC = None  # 例: "bcc@example.com" または "" (不要な場合)

# Reply-To（Noneの場合は実行時に入力を求め、""の場合は不要としてスキップ）
DEFAULT_REPLY_TO = None  # 例: "reply@example.com" または "" (不要な場合)

# 添付ファイル（空文字列の場合は実行時に入力を求めます）
# 複数のファイルを添付する場合はカンマ区切りで指定
DEFAULT_ATTACHMENTS = ""  # 例: "file1.pdf,file2.docx"

# メール送信間隔（秒）- スパム扱いを避けるための遅延時間
# 推奨値: 少量(~50通)=3-5秒, 中量(50-100通)=5-10秒, 大量(100通以上)=10秒以上
DEFAULT_SEND_DELAY = 5  # デフォルト: 5秒

# =======================================================

class EmailBulkSender:
    def __init__(self, email_address, email_password, smtp_server, smtp_port, sender_display_name=""):
        """
        メール一斉送信クラスの初期化

        Args:
            email_address: 送信元メールアドレス
            email_password: メールパスワード
            smtp_server: SMTPサーバーアドレス
            smtp_port: SMTPポート番号
            sender_display_name: 送信元表示名（オプション）
        """
        self.email_address = email_address
        self.email_password = email_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_display_name = sender_display_name
    
    def read_recipients(self, csv_file):
        """
        CSVファイルから受信者リストを読み込む

        Args:
            csv_file: CSVファイルのパス（企業,氏名,メールアドレスの形式）

        Returns:
            受信者の辞書リスト [{'company': '株式会社ABC', 'name': '山田太郎', 'email': 'yamada@example.com'}, ...]
        """
        recipients = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSVのカラム名に応じて調整
                company_key = '企業' if '企業' in row else 'company'
                name_key = '氏名' if '氏名' in row else 'name'
                email_key = 'メールアドレス' if 'メールアドレス' in row else 'email'

                recipients.append({
                    'company': row[company_key].strip(),
                    'name': row[name_key].strip(),
                    'email': row[email_key].strip()
                })
        return recipients
    
    def read_email_template(self, template_file):
        """
        メールテンプレートを読み込む（件名と本文を分離）
        
        Args:
            template_file: テンプレートファイルのパス
            
        Returns:
            (subject, body) のタプル
        """
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 件名と本文を分離（最初の行が件名、2行目は空行、3行目以降が本文）
        lines = content.split('\n')
        
        if len(lines) < 3:
            raise ValueError("テンプレートファイルの形式が正しくありません。1行目: 件名、2行目: 空行、3行目以降: 本文")
        
        subject = lines[0].strip()
        # 2行目をスキップして3行目以降を本文とする
        body = '\n'.join(lines[2:])
        
        return subject, body
    
    def create_message(self, to_email, to_name, to_company, subject_template, body_template,
                      cc=None, bcc=None, reply_to=None, attachments=None):
        """
        メールメッセージを作成

        Args:
            to_email: 宛先メールアドレス
            to_name: 宛先氏名
            to_company: 宛先企業名
            subject_template: 件名テンプレート
            body_template: 本文テンプレート
            cc: CCアドレス（カンマ区切りまたはリスト）
            bcc: BCCアドレス（カンマ区切りまたはリスト）
            reply_to: 返信先アドレス
            attachments: 添付ファイルパスのリスト

        Returns:
            MIMEMultipartメッセージオブジェクト
        """
        msg = MIMEMultipart()

        # 送信元の設定（表示名がある場合は formataddr を使用）
        if self.sender_display_name:
            msg['From'] = formataddr((self.sender_display_name, self.email_address))
        else:
            msg['From'] = self.email_address

        msg['To'] = to_email

        # 件名に企業名と氏名を展開
        subject = subject_template.replace('{企業}', to_company).replace('{氏名}', to_name)
        msg['Subject'] = Header(subject, 'utf-8')

        # CC設定
        if cc:
            if isinstance(cc, str):
                msg['Cc'] = cc
            else:
                msg['Cc'] = ', '.join(cc)

        # BCC設定
        if bcc:
            if isinstance(bcc, str):
                msg['Bcc'] = bcc
            else:
                msg['Bcc'] = ', '.join(bcc)

        # Reply-To設定
        if reply_to:
            msg['Reply-To'] = reply_to

        # 本文に企業名と氏名を展開
        body = body_template.replace('{企業}', to_company).replace('{氏名}', to_name)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 添付ファイルを追加
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        # ファイルのMIMEタイプを推測
                        filename = os.path.basename(file_path)
                        mime_type, _ = mimetypes.guess_type(file_path)
                        if mime_type is None:
                            mime_type = 'application/octet-stream'

                        # MIMEタイプを分割（例: 'image/png' -> 'image', 'png'）
                        maintype, subtype = mime_type.split('/', 1)

                        part = MIMEBase(maintype, subtype)
                        part.set_payload(f.read())
                        encoders.encode_base64(part)

                        # Content-Typeヘッダーにnameパラメータを追加
                        part.set_param('name', filename)
                        # Content-Dispositionヘッダーを設定
                        part.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(part)

        return msg
    
    def send_bulk_emails(self, csv_file, template_file,
                        cc=None, bcc=None, reply_to=None, attachments=None, delay=1):
        """
        一斉送信を実行

        Args:
            csv_file: 受信者リストCSVファイル
            template_file: メールテンプレートファイル（件名と本文）
            cc: CCアドレス
            bcc: BCCアドレス
            reply_to: 返信先アドレス
            attachments: 添付ファイルパスのリスト
            delay: メール送信間隔（秒）
        """
        # 受信者リストとテンプレートを読み込み
        recipients = self.read_recipients(csv_file)
        subject_template, body_template = self.read_email_template(template_file)
        
        print(f"\n=== 送信内容確認 ===")
        print(f"件名: {subject_template}")
        print(f"送信先: {len(recipients)}件")
        if self.sender_display_name:
            print(f"送信元: {self.sender_display_name} <{self.email_address}>")
        else:
            print(f"送信元: {self.email_address}")
        if cc:
            print(f"CC: {cc}")
        if bcc:
            print(f"BCC: {bcc}")
        if reply_to:
            print(f"Reply-To: {reply_to}")
        if attachments:
            print(f"添付ファイル: {', '.join(attachments)}")
        
        # 確認
        confirm = input("\n送信を開始しますか？ (yes/no): ")
        if confirm.lower() != 'yes':
            print("送信をキャンセルしました。")
            return
        
        # SMTP接続
        try:
            # ポート465はSSL、それ以外はTLSを使用
            if self.smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()

            server.login(self.email_address, self.email_password)
            
            # 各受信者にメール送信
            success_count = 0
            fail_count = 0
            
            for i, recipient in enumerate(recipients, 1):
                try:
                    msg = self.create_message(
                        to_email=recipient['email'],
                        to_name=recipient['name'],
                        to_company=recipient['company'],
                        subject_template=subject_template,
                        body_template=body_template,
                        cc=cc,
                        bcc=bcc,
                        reply_to=reply_to,
                        attachments=attachments
                    )

                    # 送信
                    server.send_message(msg)
                    success_count += 1
                    print(f"[{i}/{len(recipients)}] 送信成功: {recipient['company']} {recipient['name']} ({recipient['email']})")

                    # 送信間隔を設定（レート制限対策）
                    if i < len(recipients):
                        time.sleep(delay)

                except Exception as e:
                    fail_count += 1
                    print(f"[{i}/{len(recipients)}] 送信失敗: {recipient['company']} {recipient['name']} ({recipient['email']}) - エラー: {e}")
            
            server.quit()
            
            print(f"\n送信完了: 成功 {success_count}件, 失敗 {fail_count}件")
            
        except Exception as e:
            print(f"SMTP接続エラー: {e}")


def main():
    """メイン処理"""

    # メール設定
    print("=== メール一斉送信ツール ===\n")

    # SMTPサーバーの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_SMTP_SERVER:
        smtp_server = DEFAULT_SMTP_SERVER
        print(f"SMTPサーバー: {smtp_server} (設定済み)")
    else:
        smtp_server = input("SMTPサーバー (例: smtp.gmail.com): ")

    # SMTPポートの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_SMTP_PORT:
        try:
            smtp_port = int(DEFAULT_SMTP_PORT)
            print(f"SMTPポート: {smtp_port} (設定済み)")
        except ValueError:
            print(f"警告: DEFAULT_SMTP_PORT '{DEFAULT_SMTP_PORT}' が無効です。デフォルト587を使用します。")
            smtp_port = 587
    else:
        smtp_port_input = input("SMTPポート (デフォルト: 587): ").strip()
        if smtp_port_input:
            try:
                smtp_port = int(smtp_port_input)
            except ValueError:
                print(f"警告: 入力されたポート番号が無効です。デフォルト587を使用します。")
                smtp_port = 587
        else:
            smtp_port = 587

    # メールアドレスの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_EMAIL_ADDRESS:
        email_address = DEFAULT_EMAIL_ADDRESS
        print(f"送信元メールアドレス: {email_address} (設定済み)")
    else:
        email_address = input("送信元メールアドレス: ")

    # パスワードの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_EMAIL_PASSWORD:
        email_password = DEFAULT_EMAIL_PASSWORD
        print("メールパスワード: ******** (設定済み)")
    else:
        email_password = getpass("メールパスワード: ")
    
    # 送信元表示名の取得
    if SENDER_DISPLAY_NAME:
        sender_display_name = SENDER_DISPLAY_NAME
        print(f"送信元表示名: {sender_display_name} (設定済み)")
    else:
        sender_display_name = input("送信元表示名 (不要ならEnter): ").strip()
    
    # ファイルと設定
    if DEFAULT_CSV_FILE:
        csv_file = DEFAULT_CSV_FILE
        print(f"受信者リストCSVファイル: {csv_file} (設定済み)")
    else:
        csv_file = input("受信者リストCSVファイル (デフォルト: list.csv): ") or "list.csv"
    
    if DEFAULT_TEMPLATE_FILE:
        template_file = DEFAULT_TEMPLATE_FILE
        print(f"メールテンプレートファイル: {template_file} (設定済み)")
    else:
        template_file = input("メールテンプレートファイル (デフォルト: body.txt): ") or "body.txt"
    
    # オプション設定
    if DEFAULT_CC is not None:
        cc = DEFAULT_CC if DEFAULT_CC else None
        print(f"CC: {cc if cc else 'なし'} (設定済み)")
    else:
        cc = input("CC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None

    if DEFAULT_BCC is not None:
        bcc = DEFAULT_BCC if DEFAULT_BCC else None
        print(f"BCC: {bcc if bcc else 'なし'} (設定済み)")
    else:
        bcc = input("BCC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None

    if DEFAULT_REPLY_TO is not None:
        reply_to = DEFAULT_REPLY_TO if DEFAULT_REPLY_TO else None
        print(f"Reply-To: {reply_to if reply_to else 'なし'} (設定済み)")
    else:
        reply_to = input("Reply-To (不要ならEnter): ").strip() or None

    # 添付ファイル設定
    if DEFAULT_ATTACHMENTS:
        attachments_input = DEFAULT_ATTACHMENTS
        print(f"添付ファイル: {attachments_input} (設定済み)")
    else:
        attachments_input = input("添付ファイル (複数の場合はカンマ区切り、不要ならEnter): ").strip()

    # 添付ファイルのリストを作成し、存在確認
    attachments = None
    if attachments_input:
        attachments = [f.strip() for f in attachments_input.split(',')]
        # ファイルの存在確認
        for file_path in attachments:
            if not os.path.exists(file_path):
                print(f"警告: ファイルが見つかりません: {file_path}")
                confirm = input("このまま続行しますか？ (yes/no): ")
                if confirm.lower() != 'yes':
                    print("送信をキャンセルしました。")
                    return

    # 送信遅延時間の取得
    if DEFAULT_SEND_DELAY:
        send_delay = DEFAULT_SEND_DELAY
        print(f"送信間隔: {send_delay}秒 (設定済み)")
    else:
        delay_input = input("送信間隔（秒） (デフォルト: 5): ").strip()
        if delay_input:
            try:
                send_delay = float(delay_input)
            except ValueError:
                print("警告: 入力された値が無効です。デフォルト5秒を使用します。")
                send_delay = 5
        else:
            send_delay = 5

    # 送信実行
    sender = EmailBulkSender(email_address, email_password, smtp_server, smtp_port, sender_display_name)
    sender.send_bulk_emails(
        csv_file=csv_file,
        template_file=template_file,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        attachments=attachments,
        delay=send_delay
    )


if __name__ == "__main__":
    main()
