import requests
import smtplib
from email.mime.text import MIMEText
from src import config, logger

log = logger.get_logger("NOTIFIER")

def send_telegram(message):
    if not config.TELEGRAM_TOKEN or not config.CHAT_ID:
        log.warning("Telegram Config Missing. Skip.")
        return

    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": config.CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        log.error(f"Telegram Fail: {e}")

def send_email(subject, body):
    if not config.MY_EMAIL or not config.MY_PASSWORD:
        log.warning("Email Config Missing. Skip.")
        return

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = config.MY_EMAIL
        msg['To'] = config.RECEIVER_EMAIL
        
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(config.MY_EMAIL, config.MY_PASSWORD.replace(" ", ""))
            s.send_message(msg)
        log.info(f"📧 Email Sent: {subject}")
    except Exception as e:
        log.error(f"Email Fail: {e}")
