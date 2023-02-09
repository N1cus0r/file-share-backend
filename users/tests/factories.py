import factory
from faker import Faker

"""instance of Faker class that provides 
fake data for a SharedData instance"""

fake = Faker()

from users.models import CustomUser
from filesapi.tests.factories import ImageProvider

"""factory produces instances of CustomUser supplying 
the necessary fields with fake data"""


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = first_name + "." + last_name + "@example.com"
    password = fake.password()
    picture = ImageProvider.get_model_field_image()
    is_active = True
