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

urlpatterns = [
    path("create-user", CreateUser.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
    path("get-password-reset-email", GetPasswordResetEmail.as_view()),
    path("perform-password-reset", PerformPasswordReset.as_view()),
    path("activate-account", ActivateUserAccount.as_view()),
    path('get-encoded-uid', GetEditProfileUID.as_view()),
    path('edit-profile', EditProfile.as_view()),
]
