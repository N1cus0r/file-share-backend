from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class Util:
    @staticmethod
    def send_custom_email(data):
        email = EmailMultiAlternatives(
            data["email_subject"],
            data["email_content"],
            settings.EMAIL_HOST_USER,
            [data["email_to"]],
        )
        email.attach_alternative(data["html_content"], "text/html")

        email.send()
