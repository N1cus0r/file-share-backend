# Generated by Django 4.1.5 on 2023-01-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("filesapi", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shareddata",
            name="image",
        ),
        migrations.AlterField(
            model_name="shareddata",
            name="message",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="shareddata",
            name="title",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
