import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import sys
from email_bulk_sender import EmailBulkSender

# CustomTkinterの外観設定
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")


class EmailBulkSenderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("メール一括送信ツール")
        self.geometry("900x700")

        # 変数の初期化
        self.smtp_server = ctk.StringVar(value="smtp.gmail.com")
        self.smtp_port = ctk.StringVar(value="587")
        self.email_address = ctk.StringVar()
        self.email_password = ctk.StringVar()
        self.sender_display_name = ctk.StringVar()

        self.csv_file = ctk.StringVar()
        self.template_file = ctk.StringVar()
        self.attachment_files = []

        self.cc = ctk.StringVar()
        self.bcc = ctk.StringVar()
        self.reply_to = ctk.StringVar()
        self.send_delay = ctk.StringVar(value="5")

        # タブビューの作成
        self.tabview = ctk.CTkTabview(self, width=850, height=600)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # タブの追加
        self.tabview.add("基本設定")
        self.tabview.add("ファイル選択")
        self.tabview.add("オプション")
        self.tabview.add("送信実行")

        # 各タブの作成
        self.create_basic_settings_tab()
        self.create_file_selection_tab()
        self.create_options_tab()
        self.create_send_tab()

    def create_basic_settings_tab(self):
        """基本設定タブの作成"""
        tab = self.tabview.tab("基本設定")

        # スクロール可能なフレーム
        scroll_frame = ctk.CTkScrollableFrame(tab, width=800, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # SMTPサーバー設定
        ctk.CTkLabel(scroll_frame, text="SMTPサーバー設定", font=("", 16, "bold")).pack(pady=(10, 5), anchor="w")

        # SMTPサーバー
        ctk.CTkLabel(scroll_frame, text="SMTPサーバー:").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.smtp_server, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="例: smtp.gmail.com, smtp.example.com",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

        # SMTPポート
        ctk.CTkLabel(scroll_frame, text="SMTPポート:").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.smtp_port, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="例: 587 (TLS), 465 (SSL), 25 (非暗号化)",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

        # 送信者情報
        ctk.CTkLabel(scroll_frame, text="送信者情報", font=("", 16, "bold")).pack(pady=(20, 5), anchor="w")

        # メールアドレス
        ctk.CTkLabel(scroll_frame, text="メールアドレス:").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.email_address, width=400).pack(pady=5, anchor="w")

        # パスワード
        ctk.CTkLabel(scroll_frame, text="パスワード (またはアプリパスワード):").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.email_password, width=400, show="*").pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="Gmailの場合はアプリパスワードを使用してください",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

        # 送信元表示名
        ctk.CTkLabel(scroll_frame, text="送信元表示名 (オプション):").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.sender_display_name, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="例: 株式会社サンプル 営業部",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

    def create_file_selection_tab(self):
        """ファイル選択タブの作成"""
        tab = self.tabview.tab("ファイル選択")

        # スクロール可能なフレーム
        scroll_frame = ctk.CTkScrollableFrame(tab, width=800, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # CSVファイル
        ctk.CTkLabel(scroll_frame, text="受信者リストCSVファイル", font=("", 16, "bold")).pack(pady=(10, 5), anchor="w")

        csv_frame = ctk.CTkFrame(scroll_frame)
        csv_frame.pack(pady=10, fill="x")

        ctk.CTkEntry(csv_frame, textvariable=self.csv_file, width=500).pack(side="left", padx=5)
        ctk.CTkButton(csv_frame, text="ファイル選択", command=self.select_csv_file, width=100).pack(side="left", padx=5)

        ctk.CTkLabel(scroll_frame, text="CSVフォーマット: 企業,氏名,メールアドレス (または company,name,email)",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

        # テンプレートファイル
        ctk.CTkLabel(scroll_frame, text="メールテンプレートファイル", font=("", 16, "bold")).pack(pady=(20, 5), anchor="w")

        template_frame = ctk.CTkFrame(scroll_frame)
        template_frame.pack(pady=10, fill="x")

        ctk.CTkEntry(template_frame, textvariable=self.template_file, width=500).pack(side="left", padx=5)
        ctk.CTkButton(template_frame, text="ファイル選択", command=self.select_template_file, width=100).pack(side="left", padx=5)

        ctk.CTkLabel(scroll_frame, text="1行目: 件名、2行目: 空行、3行目以降: 本文\n{企業} {氏名} で置換可能",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

        # 添付ファイル
        ctk.CTkLabel(scroll_frame, text="添付ファイル (オプション)", font=("", 16, "bold")).pack(pady=(20, 5), anchor="w")

        attachment_btn_frame = ctk.CTkFrame(scroll_frame)
        attachment_btn_frame.pack(pady=10, fill="x")

        ctk.CTkButton(attachment_btn_frame, text="ファイル追加", command=self.add_attachment_files, width=100).pack(side="left", padx=5)
        ctk.CTkButton(attachment_btn_frame, text="クリア", command=self.clear_attachment_files, width=100).pack(side="left", padx=5)

        # 添付ファイルリスト表示
        self.attachment_listbox = ctk.CTkTextbox(scroll_frame, width=700, height=100)
        self.attachment_listbox.pack(pady=10, fill="x")
        self.attachment_listbox.configure(state="disabled")

    def create_options_tab(self):
        """オプション設定タブの作成"""
        tab = self.tabview.tab("オプション")

        # スクロール可能なフレーム
        scroll_frame = ctk.CTkScrollableFrame(tab, width=800, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # CC
        ctk.CTkLabel(scroll_frame, text="CC (カーボンコピー):").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.cc, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="複数の場合はカンマ区切り", text_color="gray").pack(pady=(0, 10), anchor="w")

        # BCC
        ctk.CTkLabel(scroll_frame, text="BCC (ブラインドカーボンコピー):").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.bcc, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="複数の場合はカンマ区切り", text_color="gray").pack(pady=(0, 10), anchor="w")

        # Reply-To
        ctk.CTkLabel(scroll_frame, text="Reply-To (返信先):").pack(pady=(10, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.reply_to, width=400).pack(pady=5, anchor="w")

        # 送信間隔
        ctk.CTkLabel(scroll_frame, text="送信間隔 (秒):").pack(pady=(20, 0), anchor="w")
        ctk.CTkEntry(scroll_frame, textvariable=self.send_delay, width=400).pack(pady=5, anchor="w")
        ctk.CTkLabel(scroll_frame, text="推奨: 少量(~50通)=3-5秒, 中量(50-100通)=5-10秒, 大量(100通以上)=10秒以上",
                    text_color="gray").pack(pady=(0, 10), anchor="w")

    def create_send_tab(self):
        """送信実行タブの作成"""
        tab = self.tabview.tab("送信実行")

        # プレビューボタン
        preview_frame = ctk.CTkFrame(tab)
        preview_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkButton(preview_frame, text="送信内容をプレビュー", command=self.preview_content,
                     width=200, height=40, font=("", 14, "bold")).pack(pady=10)

        # 送信ボタン
        send_frame = ctk.CTkFrame(tab)
        send_frame.pack(pady=10, padx=10, fill="x")

        self.send_button = ctk.CTkButton(send_frame, text="メール送信開始", command=self.start_sending,
                                         width=200, height=40, font=("", 14, "bold"), fg_color="green")
        self.send_button.pack(pady=10)

        # プログレスバー
        self.progress_bar = ctk.CTkProgressBar(tab, width=800)
        self.progress_bar.pack(pady=10, padx=10)
        self.progress_bar.set(0)

        # ログ表示
        ctk.CTkLabel(tab, text="送信ログ:", font=("", 14, "bold")).pack(pady=(10, 5), anchor="w", padx=10)

        self.log_textbox = ctk.CTkTextbox(tab, width=850, height=300)
        self.log_textbox.pack(pady=10, padx=10, fill="both", expand=True)

    def select_csv_file(self):
        """CSVファイル選択"""
        filename = filedialog.askopenfilename(
            title="受信者リストCSVファイルを選択",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file.set(filename)

    def select_template_file(self):
        """テンプレートファイル選択"""
        filename = filedialog.askopenfilename(
            title="メールテンプレートファイルを選択",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.template_file.set(filename)

    def add_attachment_files(self):
        """添付ファイル追加"""
        filenames = filedialog.askopenfilenames(
            title="添付ファイルを選択",
            filetypes=[("All files", "*.*")]
        )
        if filenames:
            self.attachment_files.extend(filenames)
            self.update_attachment_listbox()

    def clear_attachment_files(self):
        """添付ファイルクリア"""
        self.attachment_files.clear()
        self.update_attachment_listbox()

    def update_attachment_listbox(self):
        """添付ファイルリスト更新"""
        self.attachment_listbox.configure(state="normal")
        self.attachment_listbox.delete("1.0", "end")
        if self.attachment_files:
            for i, file in enumerate(self.attachment_files, 1):
                self.attachment_listbox.insert("end", f"{i}. {file}\n")
        else:
            self.attachment_listbox.insert("end", "添付ファイルなし")
        self.attachment_listbox.configure(state="disabled")

    def log(self, message):
        """ログに追加"""
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.update()

    def validate_inputs(self):
        """入力検証"""
        if not self.smtp_server.get():
            messagebox.showerror("エラー", "SMTPサーバーを入力してください")
            return False
        if not self.smtp_port.get():
            messagebox.showerror("エラー", "SMTPポートを入力してください")
            return False
        if not self.email_address.get():
            messagebox.showerror("エラー", "メールアドレスを入力してください")
            return False
        if not self.email_password.get():
            messagebox.showerror("エラー", "パスワードを入力してください")
            return False
        if not self.csv_file.get():
            messagebox.showerror("エラー", "受信者リストCSVファイルを選択してください")
            return False
        if not self.template_file.get():
            messagebox.showerror("エラー", "メールテンプレートファイルを選択してください")
            return False

        try:
            int(self.smtp_port.get())
        except ValueError:
            messagebox.showerror("エラー", "SMTPポートは数値で入力してください")
            return False

        try:
            float(self.send_delay.get())
        except ValueError:
            messagebox.showerror("エラー", "送信間隔は数値で入力してください")
            return False

        return True

    def preview_content(self):
        """送信内容のプレビュー"""
        if not self.validate_inputs():
            return

        try:
            sender = EmailBulkSender(
                self.email_address.get(),
                self.email_password.get(),
                self.smtp_server.get(),
                int(self.smtp_port.get()),
                self.sender_display_name.get()
            )

            # 受信者リストを読み込み
            recipients = sender.read_recipients(self.csv_file.get())
            subject_template, body_template = sender.read_email_template(self.template_file.get())

            # プレビュー内容を作成
            preview_text = f"""
=== 送信内容プレビュー ===

【基本情報】
送信元: {self.sender_display_name.get() + ' <' + self.email_address.get() + '>' if self.sender_display_name.get() else self.email_address.get()}
SMTPサーバー: {self.smtp_server.get()}:{self.smtp_port.get()}
送信先: {len(recipients)}件

【件名】
{subject_template}

【本文サンプル】（1件目の受信者で展開）
{body_template.replace('{企業}', recipients[0]['company']).replace('{氏名}', recipients[0]['name'])}

【オプション】
CC: {self.cc.get() if self.cc.get() else 'なし'}
BCC: {self.bcc.get() if self.bcc.get() else 'なし'}
Reply-To: {self.reply_to.get() if self.reply_to.get() else 'なし'}
添付ファイル: {len(self.attachment_files)}件
送信間隔: {self.send_delay.get()}秒

【送信先リスト】
"""
            for i, recipient in enumerate(recipients, 1):
                preview_text += f"{i}. {recipient['company']} {recipient['name']} ({recipient['email']})\n"

            # プレビューウィンドウを表示
            preview_window = ctk.CTkToplevel(self)
            preview_window.title("送信内容プレビュー")
            preview_window.geometry("800x600")

            preview_textbox = ctk.CTkTextbox(preview_window, width=780, height=550)
            preview_textbox.pack(pady=10, padx=10, fill="both", expand=True)
            preview_textbox.insert("1.0", preview_text)
            preview_textbox.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("エラー", f"プレビュー作成中にエラーが発生しました:\n{str(e)}")

    def start_sending(self):
        """送信開始"""
        if not self.validate_inputs():
            return

        # 確認ダイアログ
        result = messagebox.askyesno(
            "確認",
            "メール送信を開始しますか？\n送信開始後はキャンセルできません。"
        )
        if not result:
            return

        # ボタンを無効化
        self.send_button.configure(state="disabled")

        # ログクリア
        self.log_textbox.delete("1.0", "end")
        self.progress_bar.set(0)

        # 別スレッドで送信処理を実行
        thread = threading.Thread(target=self.send_emails, daemon=True)
        thread.start()

    def send_emails(self):
        """メール送信処理（別スレッドで実行）"""
        try:
            self.log("=== メール送信開始 ===")

            sender = EmailBulkSender(
                self.email_address.get(),
                self.email_password.get(),
                self.smtp_server.get(),
                int(self.smtp_port.get()),
                self.sender_display_name.get()
            )

            # 受信者リストとテンプレートを読み込み
            recipients = sender.read_recipients(self.csv_file.get())
            subject_template, body_template = sender.read_email_template(self.template_file.get())

            self.log(f"送信先: {len(recipients)}件")
            self.log(f"件名: {subject_template}")

            # オプション設定
            cc = self.cc.get() if self.cc.get() else None
            bcc = self.bcc.get() if self.bcc.get() else None
            reply_to = self.reply_to.get() if self.reply_to.get() else None
            attachments = self.attachment_files if self.attachment_files else None
            delay = float(self.send_delay.get())

            # SMTP接続して送信
            import smtplib
            import time

            try:
                # SMTP接続
                if int(self.smtp_port.get()) == 465:
                    server = smtplib.SMTP_SSL(self.smtp_server.get(), int(self.smtp_port.get()))
                else:
                    server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
                    server.starttls()

                server.login(self.email_address.get(), self.email_password.get())
                self.log("SMTP接続成功")

                success_count = 0
                fail_count = 0

                for i, recipient in enumerate(recipients, 1):
                    try:
                        msg = sender.create_message(
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

                        server.send_message(msg)
                        success_count += 1
                        self.log(f"[{i}/{len(recipients)}] 送信成功: {recipient['company']} {recipient['name']} ({recipient['email']})")

                        # プログレスバー更新
                        progress = i / len(recipients)
                        self.progress_bar.set(progress)

                        # 送信間隔
                        if i < len(recipients):
                            time.sleep(delay)

                    except Exception as e:
                        fail_count += 1
                        self.log(f"[{i}/{len(recipients)}] 送信失敗: {recipient['company']} {recipient['name']} ({recipient['email']}) - エラー: {e}")

                server.quit()
                self.log(f"\n=== 送信完了 ===")
                self.log(f"成功: {success_count}件, 失敗: {fail_count}件")

                messagebox.showinfo("完了", f"送信完了\n成功: {success_count}件, 失敗: {fail_count}件")

            except Exception as e:
                self.log(f"SMTP接続エラー: {e}")
                messagebox.showerror("エラー", f"SMTP接続エラー:\n{str(e)}")

        except Exception as e:
            self.log(f"エラー: {e}")
            messagebox.showerror("エラー", f"送信中にエラーが発生しました:\n{str(e)}")

        finally:
            # ボタンを有効化
            self.send_button.configure(state="normal")


def main():
    app = EmailBulkSenderGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
