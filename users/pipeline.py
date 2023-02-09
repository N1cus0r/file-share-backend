from .models import CustomUser
from .utils import Util


"""after the social authenticated user instance was created
the image url from the response is converted to an image file
and set as the picture attribute of CustomUser instance"""


def set_user_picture(backend, response, user=None, *args, **kwargs):
    if backend.name == "google-oauth2" and not user.picture:
        img_url = response.get("picture")
        img = Util.get_image_from_url(img_url)
        user.picture.save(f"social_auth_img_{user.pk}", img)

    if backend.name == "facebook" and not user.picture:
        img_url = response.get("picture").get("data").get("url")
        img = Util.get_image_from_url(img_url)
        user.picture.save(f"social_auth_img_{user.pk}", img)


"""activates social authenticated user account"""


def activate_user(user=None, *args, **kwargs):
    user.is_active = True
    user.save()
