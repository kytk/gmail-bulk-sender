import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
from getpass import getpass

class GmailBulkSender:
    def __init__(self, gmail_address, gmail_password):
        """
        Gmail一斉送信クラスの初期化
        
        Args:
            gmail_address: 送信元Gmailアドレス
            gmail_password: Gmailアプリパスワード
        """
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
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
                # CSVのカラム名に応じて調整してください
                # 例: '氏名', 'メールアドレス' または 'name', 'email'
                name_key = '氏名' if '氏名' in row else 'name'
                email_key = 'メールアドレス' if 'メールアドレス' in row else 'email'
                
                recipients.append({
                    'name': row[name_key].strip(),
                    'email': row[email_key].strip()
                })
        return recipients
    
    def read_body_template(self, body_file):
        """
        メール本文テンプレートを読み込む
        
        Args:
            body_file: 本文テンプレートファイルのパス
            
        Returns:
            本文テンプレート文字列
        """
        with open(body_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_message(self, to_email, to_name, subject, body_template, 
                      cc=None, bcc=None, reply_to=None):
        """
        メールメッセージを作成
        
        Args:
            to_email: 宛先メールアドレス
            to_name: 宛先氏名
            subject: 件名
            body_template: 本文テンプレート
            cc: CCアドレス（カンマ区切りまたはリスト）
            bcc: BCCアドレス（カンマ区切りまたはリスト）
            reply_to: 返信先アドレス
            
        Returns:
            MIMEMultipartメッセージオブジェクト
        """
        msg = MIMEMultipart()
        msg['From'] = self.gmail_address
        msg['To'] = to_email
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
    
    def send_bulk_emails(self, csv_file, body_file, subject, 
                        cc=None, bcc=None, reply_to=None, delay=1):
        """
        一斉送信を実行
        
        Args:
            csv_file: 受信者リストCSVファイル
            body_file: 本文テンプレートファイル
            subject: メール件名
            cc: CCアドレス
            bcc: BCCアドレス
            reply_to: 返信先アドレス
            delay: メール送信間隔（秒）
        """
        # 受信者リストと本文テンプレートを読み込み
        recipients = self.read_recipients(csv_file)
        body_template = self.read_body_template(body_file)
        
        print(f"送信先: {len(recipients)}件")
        print(f"送信元: {self.gmail_address}")
        
        # 確認
        confirm = input("送信を開始しますか？ (yes/no): ")
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
                        subject=subject,
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
    gmail_address = input("送信元Gmailアドレス: ")
    gmail_password = getpass("Gmailアプリパスワード: ")
    
    # ファイルと設定
    csv_file = input("受信者リストCSVファイル (デフォルト: list.csv): ") or "list.csv"
    body_file = input("本文テンプレートファイル (デフォルト: body.txt): ") or "body.txt"
    subject = input("メール件名: ")
    
    # オプション設定
    cc = input("CC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None
    bcc = input("BCC (複数の場合はカンマ区切り、不要ならEnter): ").strip() or None
    reply_to = input("Reply-To (不要ならEnter): ").strip() or None
    
    # 送信実行
    sender = GmailBulkSender(gmail_address, gmail_password)
    sender.send_bulk_emails(
        csv_file=csv_file,
        body_file=body_file,
        subject=subject,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        delay=1  # 1秒間隔で送信
    )


if __name__ == "__main__":
    main()
