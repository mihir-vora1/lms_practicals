from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
import smtplib
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_email_on_save(sender, instance, created, **kwargs):
    # Send an email to the user
    subject = 'Welcome to Dalton Application'
    html_message = render_to_string('user/welcome_email.html', {'user': instance})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [instance.email]
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
        email.attach_alternative(html_message, "text/html")
        smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp_server.sendmail(from_email, to_email, email.message().as_string())
        smtp_server.quit()
    except smtplib.SMTPException as e:
        print('Error while sending email: ', e)