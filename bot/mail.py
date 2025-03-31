import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Функция отправки письма
def send_email(mail_user, mail_password, to_email, header, body):
    SMTP_SERVER = "smtp.yandex.com"
    SMTP_PORT = 587

    msg = MIMEMultipart()
    msg["From"] = mail_user
    msg["To"] = to_email
    msg["Subject"] = header
    msg.attach(MIMEText(body, "plain"))

    # Подключаемся к серверу Gmail
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(mail_user, mail_password)  # Авторизация
        server.sendmail(mail_user, to_email, msg.as_string())  # Отправляем письмо


    # print(f"Письмо отправлено на {to_email}")