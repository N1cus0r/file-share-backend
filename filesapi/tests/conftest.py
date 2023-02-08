import pytest

from rest_framework.test import APIRequestFactory

from users.tests.factories import CustomUserFactory
from .factories import SharedDataFactory, ImageProvider, fake

@pytest.fixture
def new_user():
    return CustomUserFactory.create()
    

@pytest.fixture
def new_shared_data():
    return SharedDataFactory.create()


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def shared_data_form_data():
    data = {
        'title': fake.sentence(),
        'message': fake.text(),
        'file': ImageProvider.get_form_image()
    }
    
    return data