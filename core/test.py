from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import settings
from core.user.models import User
from config.wsgi import *
from django.template.loader import render_to_string

def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado')

        email_to = 'juanrestrepo246@gmail.com'

        mensaje = MIMEMultipart("Este es un mensaje")
        mensaje['from'] = settings.EMAIL_HOST_USER
        mensaje['to'] = email_to
        mensaje['subject'] = "Tienes un correo"

        content = render_to_string('send_email.html', {'user': User.objects.get(pk=1)})

        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())

        print('correo enviado correctamente')

    except Exception as e:
        print(e)
    
send_email()