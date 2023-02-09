import pytest

from filesapi.models import SharedData

"""testing the creation of a SharedData instance"""


@pytest.mark.django_db()
def test_create_shared_data_model(new_shared_data):
    assert SharedData.objects.count() == 1

    assert str(new_shared_data) == new_shared_data.title
