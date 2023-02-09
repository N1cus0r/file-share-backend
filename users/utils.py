from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class Util:
    """function sends and email to the user"""

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

    """function takes the image from the url and returns 
    a File instance of that image"""

    @staticmethod
    def get_image_from_url(img_url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(img_url).read())
        img_temp.flush()
        return File(img_temp)

    """function return encoded user id"""

    @staticmethod
    def get_encoded_user_id(user_obj):
        return urlsafe_base64_encode(force_bytes(user_obj.pk))

    """function return decoded user id"""

    @staticmethod
    def get_decoded_user_id(uid):
        return force_str(urlsafe_base64_decode(uid))
