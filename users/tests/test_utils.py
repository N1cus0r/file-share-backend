import pytest

from django.core.files.base import File
from users.utils import Util

def test_get_image_from_url():
    url = 'https://picsum.photos/200'
    image = Util.get_image_from_url(url)
    
    assert isinstance(image, File)