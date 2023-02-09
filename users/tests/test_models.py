import pytest

from users.models import CustomUser

"""testing the creation of a simple user 
from CustomUser instance"""


@pytest.mark.django_db
def test_create_user_model(new_user):
    assert CustomUser.objects.count() == 1

    assert str(new_user) == new_user.first_name

"""testing the creation of a superuser 
from CustomUser instance"""


@pytest.mark.django_db
def test_create_superuser_model(
    create_user_form_data,
):
    assert CustomUser.objects.count() == 0

    superuser = CustomUser.objects.create_superuser(**create_user_form_data)

    assert CustomUser.objects.count() == 1

    assert CustomUser.objects.last().is_superuser == superuser.is_superuser
