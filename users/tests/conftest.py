import pytest

from rest_framework.test import APIClient, APIRequestFactory
from oauth2_provider.models import Application
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .factories import CustomUserFactory, fake, ImageProvider
from filesapi.tests.factories import ImageProvider

# provides a CustomUser instance


@pytest.fixture
def new_user():
    return CustomUserFactory.create()


# provides the form data needed to create a CustomUser instance


@pytest.fixture(scope="module")
def create_user_form_data():
    first_name = fake.first_name()
    last_name = fake.first_name()
    email = first_name + "." + last_name + "@example.com"
    password = fake.password()

    form_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }

    return form_data


# provides an API Client instance


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


# provides a Request Factory instance


@pytest.fixture(scope="session")
def request_factory():
    return APIRequestFactory()


# provides an encoded version of user id


@pytest.fixture
def encoded_uid(new_user):
    return urlsafe_base64_encode(force_bytes(new_user.id))


# provides the form data needed to reset a users password


@pytest.fixture
def password_reset_data(new_user, encoded_uid):
    uid = encoded_uid
    token = PasswordResetTokenGenerator().make_token(new_user)
    password = fake.password()

    data = {"uid": uid, "token": token, "password": password}

    return data


# provides the form data needed to edit a users profile


@pytest.fixture
def edit_user_form_data(encoded_uid):
    first_name = fake.first_name()
    last_name = fake.first_name()
    picture = ImageProvider.get_form_image()

    form_data = {
        "first_name": first_name,
        "last_name": last_name,
        "picture": picture,
        "uid": encoded_uid,
    }

    return form_data
