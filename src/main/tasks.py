from __future__ import absolute_import, unicode_literals

import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from utils.tokens import account_activation_token
from celery import shared_task

User = get_user_model()


@shared_task
def send_verification_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
        current_site = 'localhost:8000'
        mail_subject = 'Activate your fubanna account.'
        message = render_to_string('main/user_activation_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.verification_uuid)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    except User.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'", user_id)


@shared_task(name="tasks.send_contact_email")
def send_contact_email(data):
    mail_subject = 'Contact Us'
    message = data.get('message')
    from_email = data.get('email')
    to_email = settings.EMAIL_HOST_USER
    email = EmailMessage(
        mail_subject, message, from_email=[from_email], to=[to_email]
    )
    email.send()
