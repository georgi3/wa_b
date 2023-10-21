# Generated by Django 4.2.6 on 2023-10-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_volunteerassignment_reject_participation"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerassignment",
            name="is_withdrawn",
            field=models.BooleanField(
                default=False,
                help_text="Applicant Withdrew their application",
                verbose_name="Is Withdrawn",
            ),
        ),
    ]
