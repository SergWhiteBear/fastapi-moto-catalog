import smtplib
import time
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

celery = Celery('tasks', broker='redis://localhost:6379',
    backend='redis://localhost:6379')

celery.conf.broker_connection_retry_on_startup = True

def get_recovery_password(username):
    email = EmailMessage()
    email['Subject'] = 'Recovery Password'
    email['From'] = SMTP_USER
    email['To'] = username

    email.set_content(
        f"""
        <div>
            <h1 style="color:blue">{username}</h1>
            <h2 style="color:blue">Recovery Password: &lt;your password&gt; or &lt;url for recovery&gt;</h2>
        </div>
        """, subtype='html'
    )
    return email

@celery.task
def send_email_recovery_form(username):
    time.sleep(2)
    email = get_recovery_password(username)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()  # Инициируем TLS
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)