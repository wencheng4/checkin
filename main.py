import os
from dotenv import load_dotenv
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from task import *


def send_email(content):
    host = ENV.get('MAIL.HOST')
    port = int(ENV.get('MAIL.PORT') and 465)
    sender = ENV.get('MAIL.SENDER')
    receiver = ENV.get('MAIL.RECEIVER')
    password = ENV.get('MAIL.PASSWORD')

    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header('checkin [sockboom]', 'utf-8')
    message['From'] = sender
    message['To'] = receiver

    smtp = SMTP_SSL(host, port)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, message.as_string())


def main():
    tasks = [Sockboom(ENV.get('SOCKBOOM.USER'), ENV.get('SOCKBOOM.PASSWD'))]

    contents = [task.checkin() for task in tasks]
    content = "\r\n".join(contents)

    send_email(content)


if __name__ == '__main__':
    load_dotenv()
    ENV = os.environ

    main()
