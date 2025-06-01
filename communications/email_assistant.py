# communications/email_assistant.py
"""
Modulo: email_assistant.py
Descrizione: Lettura e invio email via IMAP/SMTP con conferma SafetyGuard.
"""

import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from safety.safety_guard import SafetyGuard

IMAP_HOST = os.getenv("EMAIL_IMAP")
SMTP_HOST = os.getenv("EMAIL_SMTP")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

class EmailAssistant:
    def __init__(self):
        self.guard = SafetyGuard(interactive=True)

    def read_latest(self, n=5):
        with imaplib.IMAP4_SSL(IMAP_HOST) as imap:
            imap.login(EMAIL_USER, EMAIL_PASS)
            imap.select("INBOX")
            typ, data = imap.search(None, "ALL")
            ids = data[0].split()[-n:]
            messages = []
            for num in ids[::-1]:
                typ, msg_data = imap.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                messages.append({"from": msg["From"], "subject": msg["Subject"]})
            return messages

    def send_email(self, to_addr: str, subject: str, body: str):
        safe_body = self.guard.filter_text(body)
        if safe_body is None:
            return False
        msg = MIMEText(safe_body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = to_addr
        with smtplib.SMTP_SSL(SMTP_HOST) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return True
