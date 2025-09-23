import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import time
from getpass import getpass

# ==================== 設定セクション ====================
# ここで送信元情報を設定してください

# Gmailアドレス（空文字列の場合は実行時に入力を求めます）
DEFAULT_GMAIL_ADDRESS = ""  # 例: "your.email@gmail.com"

# Gmailアプリパスワード（空文字列の場合は実行時に入力を求めます）
# セキュリティ上、ここには記載せず実行時に入力することを推奨
DEFAULT_GMAIL_PASSWORD = ""

# 送信元表示名（空文字列の場合はメールアドレスのみ表示）
SENDER_DISPLAY_NAME = ""  # 例: "株式会社サンプル 営業部"

# =======================================================

class GmailBulkSender:
    def __init__(self, gmail_address, gmail_password, sender_display_name=""):
        """
        Gmail一斉送信クラスの初期化
        
        Args:
            gmail_address: 送信元Gmailアドレス
            gmail_password: Gmailアプリパスワード
            sender_display_name: 送信元表示名（オプション）
        """
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        self.sender_display_name = sender_display_name
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def read_recipients(self, csv_file):
        """
        CSVファイルから受信者リストを読み込む
        
        Args:
            csv_file: CSVファイルのパス（氏名,メールアドレスの形式）
            
        Returns:
            受信者の辞書リスト [{'name': '山田太郎', 'email': 'yamada@example.com'}, ...]
        """
        recipients = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSVのカラム名に応じて調整
                name_key = '氏名' if '氏名' in row else 'name'
                email_key = 'メールアドレス' if 'メールアドレス' in row else 'email'
                
                recipients.append({
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
    
    def create_message(self, to_email, to_name, subject_template, body_template, 
                      cc=None, bcc=None, reply_to=None):
        """
        メールメッセージを作成
        
        Args:
            to_email: 宛先メールアドレス
            to_name: 宛先氏名
            subject_template: 件名テンプレート
            body_template: 本文テンプレート
            cc: CCアドレス（カンマ区切りまたはリスト）
            bcc: BCCアドレス（カンマ区切りまたはリスト）
            reply_to: 返信先アドレス
            
        Returns:
            MIMEMultipartメッセージオブジェクト
        """
        msg = MIMEMultipart()
        
        # 送信元の設定（表示名がある場合は formataddr を使用）
        if self.sender_display_name:
            msg['From'] = formataddr((self.sender_display_name, self.gmail_address))
        else:
            msg['From'] = self.gmail_address
            
        msg['To'] = to_email
        
        # 件名に氏名を展開
        subject = subject_template.replace('{氏名}', to_name)
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
        
        # 本文に氏名を展開
        body = body_template.replace('{氏名}', to_name)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        return msg
    
    def send_bulk_emails(self, csv_file, template_file, 
                        cc=None, bcc=None, reply_to=None, delay=1):
        """
        一斉送信を実行
        
        Args:
            csv_file: 受信者リストCSVファイル
            template_file: メールテンプレートファイル（件名と本文）
            cc: CCアドレス
            bcc: BCCアドレス
            reply_to: 返信先アドレス
            delay: メール送信間隔（秒）
        """
        # 受信者リストとテンプレートを読み込み
        recipients = self.read_recipients(csv_file)
        subject_template, body_template = self.read_email_template(template_file)
        
        print(f"\n=== 送信内容確認 ===")
        print(f"件名: {subject_template}")
        print(f"送信先: {len(recipients)}件")
        if self.sender_display_name:
            print(f"送信元: {self.sender_display_name} <{self.gmail_address}>")
        else:
            print(f"送信元: {self.gmail_address}")
        if cc:
            print(f"CC: {cc}")
        if bcc:
            print(f"BCC: {bcc}")
        if reply_to:
            print(f"Reply-To: {reply_to}")
        
        # 確認
        confirm = input("\n送信を開始しますか？ (yes/no): ")
        if confirm.lower() != 'yes':
            print("送信をキャンセルしました。")
            return
        
        # SMTP接続
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_address, self.gmail_password)
            
            # 各受信者にメール送信
            success_count = 0
            fail_count = 0
            
            for i, recipient in enumerate(recipients, 1):
                try:
                    msg = self.create_message(
                        to_email=recipient['email'],
                        to_name=recipient['name'],
                        subject_template=subject_template,
                        body_template=body_template,
                        cc=cc,
                        bcc=bcc,
                        reply_to=reply_to
                    )
                    
                    # 送信
                    server.send_message(msg)
                    success_count += 1
                    print(f"[{i}/{len(recipients)}] 送信成功: {recipient['name']} ({recipient['email']})")
                    
                    # 送信間隔を設定（Gmail制限対策）
                    if i < len(recipients):
                        time.sleep(delay)
                        
                except Exception as e:
                    fail_count += 1
                    print(f"[{i}/{len(recipients)}] 送信失敗: {recipient['name']} ({recipient['email']}) - エラー: {e}")
            
            server.quit()
            
            print(f"\n送信完了: 成功 {success_count}件, 失敗 {fail_count}件")
            
        except Exception as e:
            print(f"SMTP接続エラー: {e}")


def main():
    """メイン処理"""
    
    # Gmail設定
    print("=== Gmail一斉送信ツール ===\n")
    
    # Gmailアドレスの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_GMAIL_ADDRESS:
        gmail_address = DEFAULT_GMAIL_ADDRESS
        print(f"送信元Gmailアドレス: {gmail_address} (設定済み)")
    else:
        gmail_address = input("送信元Gmailアドレス: ")
    
    # アプリパスワードの取得（デフォルト値がある場合はそれを使用）
    if DEFAULT_GMAIL_PASSWORD:
        gmail_password = DEFAULT_GMAIL_PASSWORD
        print("Gmailアプリパスワード: ******** (設定済み)")
    else:
        gmail_password = getpass("Gmailアプリパスワード: ")
    
    # 送信元表示名の取得
    if SENDER_DISPLAY_NAME:
        sender_display_name = SENDER_DISPLAY_NAME
        print(f"送信元表示名: {sender_display_name} (設定済み)")
    else:
        sender_display_name = input("送信元表示名 (不要ならEnter): ").strip()
    
    # ファイルと設定
    csv_file = input("受信者リストCSVファイル (デフォルト: list.csv): ") or "list.csv"
    template_file = input("メールテンプレートファイル (デフォルト: body.txt): ") or "body.txt"
    
    # オプション設定
    cc = input("CC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None
    bcc = input("BCC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None
    reply_to = input("Reply-To (不要ならEnter): ").strip() or None
    
    # 送信実行
    sender = GmailBulkSender(gmail_address, gmail_password, sender_display_name)
    sender.send_bulk_emails(
        csv_file=csv_file,
        template_file=template_file,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        delay=1  # 1秒間隔で送信
    )


if __name__ == "__main__":
    main()
