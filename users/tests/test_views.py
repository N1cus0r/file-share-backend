import pytest

from django.urls import reverse
from rest_framework.test import force_authenticate
from users.views import (
    GetUserInfo,
    GetEditProfileUID,
    EditProfile,
    ActivateUserAccount,
    PerformPasswordReset,
)

"""testing the creation of a CustomUser instance from
the API endpoint via POST request"""


@pytest.mark.django_db
def test_create_user_view(create_user_form_data, api_client):
    response = api_client.post(
        path=reverse("users:create-user"), data=create_user_form_data
    )

    assert response.status_code == 201

"""testing the activation of a CustomUser instance using
an API endpoint via PATCH request"""


@pytest.mark.django_db
def test_activate_account_view(encoded_uid, request_factory):
    view = ActivateUserAccount.as_view()
    request = request_factory.patch(
        reverse("users:activate-account"), data={"uid": encoded_uid}
    )

    response = view(request)

    assert response.status_code == 200

'''testing the retrieve of a CustomUser serialized
instance using an API endpoint via GET request'''

@pytest.mark.django_db
def test_get_user_info_view(new_user, request_factory):
    view = GetUserInfo.as_view()
    request = request_factory.get(
        path=reverse("users:get-user-info"), data={"email": new_user.email}
    )
    force_authenticate(request, user=new_user)

    response = view(request)

    assert response.status_code == 200

    assert response.data is not None


'''testing retrieving a CustomUser instance encoded id
using an API endpoint via GET request'''


@pytest.mark.django_db
def test_get_edit_profile_encoded_uid_view(new_user, request_factory):
    view = GetEditProfileUID.as_view()
    request = request_factory.get(
        path=reverse("users:get-encoded-uid"), data={"email": new_user.email}
    )
    force_authenticate(request, user=new_user)

    response = view(request)

    assert response.status_code == 200

    assert isinstance(response.data, str)

'''testing editing a CustomUser instance
using an API endpoint via PATCH request'''


@pytest.mark.django_db
def test_edit_profile_view(new_user, request_factory, edit_user_form_data):
    view = EditProfile.as_view()
    request = request_factory.patch(
        reverse("users:edit-profile"), data=edit_user_form_data
    )
    force_authenticate(request, user=new_user)

    response = view(request)

    print(response.data)

    assert response.status_code == 200

'''testing resetting a CustomUser instance password
using an API endpoint via PATCH request'''


@pytest.mark.django_db
def test_perform_password_reset_view(request_factory, password_reset_data):
    view = PerformPasswordReset.as_view()
    request = request_factory.patch(
        reverse("users:perform-password-reset"), data=password_reset_data
    )

    response = view(request)

    assert response.status_code == 200
