# Generated by Django 4.2.19 on 2025-02-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_volunteeringevents_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerassignment",
            name="attended",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Attended"
            ),
        ),
    ]
