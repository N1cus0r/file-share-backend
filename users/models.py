from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, password, picture, last_name=""):

        if not email:
            raise ValueError("You must provide an email address")
        elif not first_name:
            raise ValueError("You must provide your first name")

        email = self.normalize_email(email)
        first_name = first_name.title()
        last_name = last_name.title()

        user = self.model(
            email=email, first_name=first_name, last_name=last_name, picture=picture
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, password, last_name=""):
        user = self.create_user(email, first_name, password, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.first_name
