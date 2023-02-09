import factory
from faker import Faker
from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile

from filesapi.models import SharedData

"""instance of Faker class that provides 
fake data for a SharedData instance"""

fake = Faker()

"""custom class which provider images temporary stored in memory
for SharedData instances and CustomUser instances"""


class ImageProvider:
    @staticmethod
    def get_model_field_image():
        image = Image.new(
            "RGBA",
            size=(50, 50),
            color=tuple(fake.pyint(min_value=0, max_value=225) for _ in range(3)),
        )
        file = BytesIO(image.tobytes())
        file.name = "test.png"
        file.seek(0)

        return ContentFile(file.read(), "test.png")

    @staticmethod
    def get_form_image():
        file = BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file


"""factory produces instances of SharedData supplying 
the file field with an image and other fields
with fake data"""


class SharedDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SharedData

    title = fake.sentence()
    message = fake.text()
    file = ImageProvider.get_model_field_image()
