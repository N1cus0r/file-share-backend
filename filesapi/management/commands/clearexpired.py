from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import SharedData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        queryset = SharedData.objects.filter(
            date_created__lt=timezone.now() - timedelta(days=1)
        )
        nub_of_objects = queryset.count()
        queryset.delete()

        self.stdout.write(f"{nub_of_objects} expired records found.")
