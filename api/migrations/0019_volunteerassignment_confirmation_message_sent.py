# Generated by Django 4.2.6 on 2024-02-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_volunteerassignment_has_confirmed"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerassignment",
            name="confirmation_message_sent",
            field=models.BooleanField(default=False),
        ),
    ]
