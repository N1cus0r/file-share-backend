import pytest

from rest_framework.test import APIRequestFactory

from users.tests.factories import CustomUserFactory
from .factories import SharedDataFactory, ImageProvider, fake

# provides a CustomUser instance in the tests


@pytest.fixture
def new_user():
    return CustomUserFactory.create()


# provides a SharedData instance


@pytest.fixture
def new_shared_data():
    return SharedDataFactory.create()


# provides a Request Factory instance


@pytest.fixture
def request_factory():
    return APIRequestFactory()


# provides the form data needed to create a SharedData instance


@pytest.fixture
def shared_data_form_data():
    data = {
        "title": fake.sentence(),
        "message": fake.text(),
        "file": ImageProvider.get_form_image(),
    }

    return data
