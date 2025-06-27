import smtplib
from email.message import EmailMessage
import requests
import os

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")

def send_email(ip, payload):
    try:
        msg = EmailMessage()
        msg.set_content(f"SQL Injection Detected!\nIP: {ip}\nPayload: {payload}")
        msg['Subject'] = '⚠️ SQL Injection Alert'
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")

def send_slack(payload):
    if not SLACK_WEBHOOK:
        print("Slack webhook not set.")
        return
    msg = {'text': f'⚠️ SQL Injection Detected!\nPayload: {payload}'}
    try:
        requests.post(SLACK_WEBHOOK, json=msg, timeout=3)
    except Exception as e:
        print(f"Slack error: {e}")
