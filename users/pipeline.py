from .models import CustomUser


def set_user_picture(backend, response, user=None, *args, **kwargs):
    if backend.name == "google-oauth2":
        user.picture = response.get("picture")
        user.save()

    if backend.name == "facebook":
        user.picture = response.get("picture").get("data").get("url")
        user.save()

    return


def activate_user(user=None, *args, **kwargs):
    user.is_active = True
    user.save()
