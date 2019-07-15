import logging
import uuid
import smtplib

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.translation import activate

from accounts.models import Token
from celery import shared_task

User = get_user_model()
activate('en')


@shared_task(bind=True)
def send_login_email_task(self, email):
    try:
        uid = str(uuid.uuid4())
        Token.objects.create(email=email, uid=uid)
        current_site = 'localhost:8000'
        mail_subject = 'Activate your Fubanna account.'
        message = render_to_string('accounts/login_activation_email.html', {
            'domain': current_site,
            'uid': uid
        })
        email = EmailMessage(mail_subject, message, to=[email])
        email.send()
    except Token.DoesNotExist:
        logging.warning(
            "Tried to send activation email to non-existing user '%s'", email)
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True)
def send_register_email_task(self, data):
    try:
        email = data.get('email')
        mail_subject = "Request to be an Agent"
        message = render_to_string('accounts/agent_verification_email.html', {
            'email': email,
            'phone_number': data.get('phone_number'),
            'screen_name': data.get('screen_name')
        })
        email = "faisallarai@gmail.com"
        email = EmailMessage(mail_subject, message, to=[email])
        email.send()
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc)
