from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings

from .models import CustomUser
from .utils import Util


"""checks if an user with the provided email exists
and creates an inactive CustomUser instance, then
sends an email for account activation"""


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password"]

    def validate(self, data):
        email = data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create(
            **validated_data, password=make_password(password)
        )

        user_id_b64 = urlsafe_base64_encode(force_bytes(user.pk))
        absURL = settings.CLIENT_HOST_URL + "/activate-account/" + str(user_id_b64)

        html_content = render_to_string(
            "account_activation_email.html", {"redirect_url": absURL}
        )
        text_content = strip_tags(html_content)

        email_data = {
            "email_to": user.email,
            "email_subject": "Account Activation",
            "email_content": text_content,
            "html_content": html_content,
        }

        Util.send_custom_email(email_data)

        return user


"""activates a CustomUser instance"""


class ActivateAccountSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)

    class Meta:
        fields = ["uid"]

    def validate(self, data):
        uid = data.get("uid")

        user_id = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=user_id)

        user.is_active = True
        user.save()

        return data


"""serializes the CustomUser model"""


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "picture"]


"""takes the provided email for password reset and sends
an email to reset the password"""


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]

    def validate(self, data):
        email = data.get("email")
        queryset = CustomUser.objects.filter(email=email)
        if queryset.exists():
            user = queryset[0]
            user_id_b64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            absURL = (
                settings.CLIENT_HOST_URL
                + "/password-reset/"
                + f"{user_id_b64}/{str(token)}"
            )

            html_content = render_to_string(
                "password_reset_email.html", {"redirect_url": absURL}
            )
            text_content = strip_tags(html_content)

            email_data = {
                "email_to": user.email,
                "email_subject": "Password Reset",
                "email_content": text_content,
                "html_content": html_content,
            }
            Util.send_custom_email(email_data)

            return data

        raise serializers.ValidationError("User with this email does not exist")


"""takes the password reset token as well as the encoded user id
and updates the password with the provided password"""


class PerformPasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ["uid", "token", "password"]

    def validate(self, data):
        uid = data.get("uid")
        token = data.get("token")
        password = data.get("password")

        user_id = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid token for this user")

        user.set_password(password)
        user.save()

        return user


"""takes the encoded user id as well as the data
to change the user profile"""


class EditProfileSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["uid", "first_name", "last_name", "picture"]

    def validate(self, data):
        user_id = Util.get_decoded_user_id(data.pop("uid"))
        queryset = CustomUser.objects.filter(pk=user_id)

        if not queryset.exists():
            raise serializers.ValidationError("Encoded UID does not match users id")

        data["uid"] = user_id

        return data

    def create(self, validated_data):
        user = CustomUser.objects.get(pk=validated_data["uid"])

        if validated_data.get("first_name"):
            user.first_name = validated_data["first_name"]

        if validated_data.get("last_name"):
            user.last_name = validated_data["last_name"]

        if validated_data.get("picture"):
            user.picture = validated_data["picture"]

        user.save()
        return user
