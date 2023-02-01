import random
from string import ascii_uppercase

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.validators import FileExtensionValidator


def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = (
        model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    )
    if not other_refs_exist:
        instance_file_field.delete(False)


@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


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
