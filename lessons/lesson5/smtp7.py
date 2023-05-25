from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib,os

load_dotenv('.env')

def send_mail(subject:str,message:str,to_email:str) -> bool:
    sender = os.environ.get('smtp_email')
    password = os.environ.get('smtp_password')

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject']  = subject
    msg['From'] = sender
    msg['To'] = to_email
    try:
        server.login(sender,password)
        server.send_message(msg)
        return True
    except Exception as error:
        return f'Error: {error}'
    
# print(send_mail('SMTP PYTHON',' Hello World','@gmail.com'))

emails = ['@gmail.com']
print(send_mail('SMTP PYTHON',' Hello World',emails))


