import pytest

from django.urls import reverse
from rest_framework.test import force_authenticate


from filesapi.views import CreateSharedDataInstance, GetDataInstance

"""testing the creation of a SharedData instance from
the API endpoint via POST request"""


@pytest.mark.django_db
def test_create_shared_data_instance_view(
    new_user, shared_data_form_data, request_factory
):
    view = CreateSharedDataInstance.as_view()
    request = request_factory.post(
        path=reverse("files:upload-data"), data=shared_data_form_data
    )

    force_authenticate(request, user=new_user)

    response = view(request)

    assert response.status_code == 201

    assert response.data.get("instance") and response.data.get("url")


"""testing the retrieving of a SharedData instance
from the API endpoint via GET request"""


@pytest.mark.django_db
def test_get_shared_data_instance(new_shared_data, request_factory):
    view = GetDataInstance.as_view()
    request = request_factory.get(
        path=reverse("files:get-data-instance"), data={"code": new_shared_data.code}
    )

    response = view(request)

    assert response.status_code == 200
