#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国際化（i18n）モジュール
言語データを管理し、UIテキストの多言語対応を提供します
"""

import locale
import sys

# サポートされている言語
SUPPORTED_LANGUAGES = ['ja', 'en']

# 言語データ辞書
TEXTS = {
    'ja': {
        # 共通
        'app_title_generic': 'メール一括送信ツール',
        'app_title_gmail': 'Gmail一括送信ツール',
        'yes': 'yes',
        'no': 'no',

        # タブ名（GUI）
        'tab_basic': '基本設定',
        'tab_files': 'ファイル選択',
        'tab_options': 'オプション',
        'tab_send': '送信実行',
        'tab_language': '言語設定',

        # 基本設定タブ
        'smtp_settings': 'SMTPサーバー設定',
        'smtp_server': 'SMTPサーバー:',
        'smtp_server_example': '例: smtp.gmail.com, smtp.example.com',
        'smtp_port': 'SMTPポート:',
        'smtp_port_example': '例: 587 (TLS), 465 (SSL), 25 (非暗号化)',
        'sender_info': '送信者情報',
        'email_address': 'メールアドレス:',
        'password': 'パスワード (またはアプリパスワード):',
        'password_hint': 'Gmailの場合はアプリパスワードを使用してください',
        'sender_display_name': '送信元表示名 (オプション):',
        'sender_display_name_example': '例: 株式会社サンプル 営業部',
        'gmail_address': '送信元Gmailアドレス:',
        'gmail_app_password': 'Gmailアプリパスワード:',

        # ファイル選択タブ
        'recipient_list': '受信者リスト',
        'csv_file': 'CSVファイル:',
        'select_file': 'ファイル選択',
        'csv_description': 'フォーマット: 企業,氏名,メールアドレス',
        'email_template': 'メールテンプレート',
        'template_file': 'テンプレートファイル:',
        'template_description': '1行目: 件名、2行目: 空行、3行目以降: 本文',
        'attachments': '添付ファイル (オプション)',
        'add_file': 'ファイル追加',
        'remove_file': '削除',
        'no_attachments': '添付ファイルなし',

        # オプションタブ
        'email_options': 'メールオプション',
        'cc': 'CC (複数の場合はカンマ区切り):',
        'bcc': 'BCC (複数の場合はカンマ区切り):',
        'reply_to': 'Reply-To:',
        'sending_options': '送信オプション',
        'send_delay': '送信間隔 (秒):',
        'send_delay_hint': '各メール送信の間隔（デフォルト: 5秒）',

        # 送信実行タブ
        'preview': 'プレビュー',
        'preview_button': '送信内容をプレビュー',
        'send_execution': '送信実行',
        'send_button': 'メール送信開始',
        'progress': '進捗状況',
        'log': 'ログ',

        # 言語設定タブ
        'language_setting': '言語設定',
        'language': '言語 / Language:',
        'language_note': '言語を変更した場合、アプリケーションを再起動してください。',

        # ダイアログ・メッセージ
        'select_csv': 'CSVファイルを選択',
        'select_template': 'テンプレートファイルを選択',
        'select_attachment': '添付ファイルを選択',
        'error': 'エラー',
        'info': '情報',
        'warning': '警告',
        'confirm': '確認',
        'success': '成功',

        # エラーメッセージ
        'error_missing_fields': '必須項目が入力されていません',
        'error_missing_email': 'メールアドレスを入力してください',
        'error_missing_password': 'パスワードを入力してください',
        'error_missing_csv': 'CSVファイルを選択してください',
        'error_missing_template': 'テンプレートファイルを選択してください',
        'error_invalid_delay': '送信間隔は正の数値を入力してください',
        'error_send_failed': '送信中にエラーが発生しました',
        'error_file_not_found': 'ファイルが見つかりません: {0}',

        # 成功メッセージ
        'send_complete': '送信完了: 成功 {0}件, 失敗 {1}件',
        'preview_title': 'プレビュー',

        # プレビュー内容
        'preview_subject': '件名: {0}',
        'preview_recipients': '送信先: {0}件',
        'preview_sender': '送信元: {0}',
        'preview_cc': 'CC: {0}',
        'preview_bcc': 'BCC: {0}',
        'preview_reply_to': 'Reply-To: {0}',
        'preview_attachments': '添付ファイル: {0}',
        'preview_delay': '送信間隔: {0}秒',

        # 送信確認
        'confirm_send': '送信を開始してもよろしいですか？',
        'sending': '送信中...',
        'send_success': '[{0}/{1}] 送信成功: {2} {3} ({4})',
        'send_failed': '[{0}/{1}] 送信失敗: {2} {3} ({4}) - {5}',

        # CLI版のメッセージ
        'cli_title': '=== メール一括送信ツール ===',
        'cli_gmail_title': '=== Gmail一括送信ツール ===',
        'cli_smtp_server': 'SMTPサーバー (例: smtp.gmail.com)',
        'cli_smtp_port': 'SMTPポート (デフォルト: 587)',
        'cli_email_address': '送信元メールアドレス',
        'cli_email_password': 'メールパスワード',
        'cli_gmail_address': '送信元Gmailアドレス',
        'cli_gmail_password': 'Gmailアプリパスワード',
        'cli_sender_name': '送信元表示名 (不要ならEnter)',
        'cli_csv_file': '受信者リストCSVファイル (デフォルト: list.csv)',
        'cli_template_file': 'メールテンプレートファイル (デフォルト: body.txt)',
        'cli_cc': 'CC (複数の場合はカンマ区切り、不要ならEnter)',
        'cli_bcc': 'BCC (複数の場合はカンマ区切り、不要ならEnter)',
        'cli_reply_to': 'Reply-To (不要ならEnter)',
        'cli_confirm_header': '\n=== 送信内容確認 ===',
        'cli_confirm_send': '\n送信を開始しますか？ (yes/no)',
        'cli_cancelled': '送信をキャンセルしました',
        'cli_language': '言語 / Language (ja/en, デフォルト: {0})',
    },
    'en': {
        # Common
        'app_title_generic': 'Email Bulk Sender',
        'app_title_gmail': 'Gmail Bulk Sender',
        'yes': 'yes',
        'no': 'no',

        # Tab names (GUI)
        'tab_basic': 'Basic Settings',
        'tab_files': 'File Selection',
        'tab_options': 'Options',
        'tab_send': 'Send',
        'tab_language': 'Language',

        # Basic settings tab
        'smtp_settings': 'SMTP Server Settings',
        'smtp_server': 'SMTP Server:',
        'smtp_server_example': 'e.g., smtp.gmail.com, smtp.example.com',
        'smtp_port': 'SMTP Port:',
        'smtp_port_example': 'e.g., 587 (TLS), 465 (SSL), 25 (unencrypted)',
        'sender_info': 'Sender Information',
        'email_address': 'Email Address:',
        'password': 'Password (or App Password):',
        'password_hint': 'Use App Password for Gmail',
        'sender_display_name': 'Sender Display Name (Optional):',
        'sender_display_name_example': 'e.g., Sample Corp Sales Dept',
        'gmail_address': 'Sender Gmail Address:',
        'gmail_app_password': 'Gmail App Password:',

        # File selection tab
        'recipient_list': 'Recipient List',
        'csv_file': 'CSV File:',
        'select_file': 'Select File',
        'csv_description': 'Format: Company,Name,Email',
        'email_template': 'Email Template',
        'template_file': 'Template File:',
        'template_description': 'Line 1: Subject, Line 2: Empty, Line 3+: Body',
        'attachments': 'Attachments (Optional)',
        'add_file': 'Add File',
        'remove_file': 'Remove',
        'no_attachments': 'No attachments',

        # Options tab
        'email_options': 'Email Options',
        'cc': 'CC (comma-separated for multiple):',
        'bcc': 'BCC (comma-separated for multiple):',
        'reply_to': 'Reply-To:',
        'sending_options': 'Sending Options',
        'send_delay': 'Send Delay (seconds):',
        'send_delay_hint': 'Interval between each email (default: 5 seconds)',

        # Send execution tab
        'preview': 'Preview',
        'preview_button': 'Preview Email Content',
        'send_execution': 'Send Execution',
        'send_button': 'Start Sending',
        'progress': 'Progress',
        'log': 'Log',

        # Language settings tab
        'language_setting': 'Language Settings',
        'language': 'Language / 言語:',
        'language_note': 'Please restart the application after changing the language.',

        # Dialogs & Messages
        'select_csv': 'Select CSV File',
        'select_template': 'Select Template File',
        'select_attachment': 'Select Attachment File',
        'error': 'Error',
        'info': 'Information',
        'warning': 'Warning',
        'confirm': 'Confirm',
        'success': 'Success',

        # Error messages
        'error_missing_fields': 'Required fields are missing',
        'error_missing_email': 'Please enter email address',
        'error_missing_password': 'Please enter password',
        'error_missing_csv': 'Please select CSV file',
        'error_missing_template': 'Please select template file',
        'error_invalid_delay': 'Please enter a positive number for send delay',
        'error_send_failed': 'Error occurred during sending',
        'error_file_not_found': 'File not found: {0}',

        # Success messages
        'send_complete': 'Sending complete: {0} succeeded, {1} failed',
        'preview_title': 'Preview',

        # Preview content
        'preview_subject': 'Subject: {0}',
        'preview_recipients': 'Recipients: {0}',
        'preview_sender': 'Sender: {0}',
        'preview_cc': 'CC: {0}',
        'preview_bcc': 'BCC: {0}',
        'preview_reply_to': 'Reply-To: {0}',
        'preview_attachments': 'Attachments: {0}',
        'preview_delay': 'Send delay: {0} seconds',

        # Send confirmation
        'confirm_send': 'Are you sure you want to start sending?',
        'sending': 'Sending...',
        'send_success': '[{0}/{1}] Success: {2} {3} ({4})',
        'send_failed': '[{0}/{1}] Failed: {2} {3} ({4}) - {5}',

        # CLI messages
        'cli_title': '=== Email Bulk Sender ===',
        'cli_gmail_title': '=== Gmail Bulk Sender ===',
        'cli_smtp_server': 'SMTP Server (e.g., smtp.gmail.com)',
        'cli_smtp_port': 'SMTP Port (default: 587)',
        'cli_email_address': 'Sender Email Address',
        'cli_email_password': 'Email Password',
        'cli_gmail_address': 'Sender Gmail Address',
        'cli_gmail_password': 'Gmail App Password',
        'cli_sender_name': 'Sender Display Name (press Enter to skip)',
        'cli_csv_file': 'Recipient List CSV File (default: list.csv)',
        'cli_template_file': 'Email Template File (default: body.txt)',
        'cli_cc': 'CC (comma-separated for multiple, press Enter to skip)',
        'cli_bcc': 'BCC (comma-separated for multiple, press Enter to skip)',
        'cli_reply_to': 'Reply-To (press Enter to skip)',
        'cli_confirm_header': '\n=== Confirm Sending Details ===',
        'cli_confirm_send': '\nStart sending? (yes/no)',
        'cli_cancelled': 'Sending cancelled',
        'cli_language': 'Language / 言語 (ja/en, default: {0})',
    }
}


class I18n:
    """国際化クラス"""

    def __init__(self, lang=None):
        """
        初期化

        Args:
            lang: 言語コード ('ja' または 'en')。Noneの場合はシステム言語を自動検出
        """
        if lang is None:
            lang = self._detect_system_language()

        self.lang = lang if lang in SUPPORTED_LANGUAGES else 'en'

    def _detect_system_language(self):
        """システムの言語を自動検出"""
        try:
            # Python 3.11+ では getlocale() を使用
            system_locale = locale.getlocale()[0]
            if system_locale and system_locale.startswith('ja'):
                return 'ja'
        except:
            pass
        return 'en'

    def get(self, key, *args):
        """
        言語キーに対応するテキストを取得

        Args:
            key: テキストキー
            *args: フォーマット引数

        Returns:
            ローカライズされたテキスト
        """
        text = TEXTS.get(self.lang, {}).get(key, key)
        if args:
            return text.format(*args)
        return text

    def set_language(self, lang):
        """言語を設定"""
        if lang in SUPPORTED_LANGUAGES:
            self.lang = lang

    def get_language(self):
        """現在の言語を取得"""
        return self.lang

    def get_supported_languages(self):
        """サポートされている言語のリストを取得"""
        return SUPPORTED_LANGUAGES.copy()


# グローバルインスタンス
_i18n_instance = None


def get_i18n(lang=None):
    """
    I18nのグローバルインスタンスを取得

    Args:
        lang: 言語コード。Noneの場合は既存インスタンスまたは自動検出

    Returns:
        I18nインスタンス
    """
    global _i18n_instance
    if _i18n_instance is None or lang is not None:
        _i18n_instance = I18n(lang)
    return _i18n_instance


def t(key, *args):
    """
    テキストを取得する便利関数

    Args:
        key: テキストキー
        *args: フォーマット引数

    Returns:
        ローカライズされたテキスト
    """
    return get_i18n().get(key, *args)


if __name__ == '__main__':
    # テスト
    print("Testing i18n module...")

    # 日本語テスト
    i18n_ja = I18n('ja')
    print(f"\nJapanese (ja):")
    print(f"  app_title_generic: {i18n_ja.get('app_title_generic')}")
    print(f"  smtp_server: {i18n_ja.get('smtp_server')}")
    print(f"  send_complete: {i18n_ja.get('send_complete', 10, 2)}")

    # 英語テスト
    i18n_en = I18n('en')
    print(f"\nEnglish (en):")
    print(f"  app_title_generic: {i18n_en.get('app_title_generic')}")
    print(f"  smtp_server: {i18n_en.get('smtp_server')}")
    print(f"  send_complete: {i18n_en.get('send_complete', 10, 2)}")

    # 自動検出テスト
    i18n_auto = I18n()
    print(f"\nAuto-detected language: {i18n_auto.get_language()}")
    print(f"  app_title_generic: {i18n_auto.get('app_title_generic')}")
