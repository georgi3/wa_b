# Generated by Django 4.2.19 on 2025-02-20 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_volunteerassignment_attended"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="volunteerassignment",
            name="has_confirmed",
        ),
    ]
