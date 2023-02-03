import random
from string import ascii_uppercase
from django.db import models


def create_unique_code():
    while True:
        code = "".join(random.choices(ascii_uppercase, k=6))
        if not SharedData.objects.filter(code=code).exists():
            return code

class SharedData(models.Model):
    title = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, upload_to="files")
    code = models.CharField(max_length=6, unique=True, default=create_unique_code)

    def __str__(self):
        return self.title
