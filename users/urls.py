from django.urls import path
from .views import (
    CreateUser,
    GetUserInfo,
    GetPasswordResetEmail,
    PerformPasswordReset,
    ActivateUserAccount,
    GetEditProfileUID,
    EditProfile,
)

app_name = "users"

urlpatterns = [
    path("create-user", CreateUser.as_view(), name="create-user"),
    path("get-user-info", GetUserInfo.as_view(), name="get-user-info"),
    path("get-password-reset-email", GetPasswordResetEmail.as_view()),
    path("perform-password-reset", PerformPasswordReset.as_view(), name='perform-password-reset'),
    path("activate-account", ActivateUserAccount.as_view(), name='activate-account'),
    path("get-encoded-uid", GetEditProfileUID.as_view(), name="get-encoded-uid"),
    path("edit-profile", EditProfile.as_view(), name='edit-profile'),
]
