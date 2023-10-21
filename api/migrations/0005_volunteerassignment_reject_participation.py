# Generated by Django 4.2.6 on 2023-10-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_contactform_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerassignment",
            name="reject_participation",
            field=models.BooleanField(
                default=False,
                help_text="Check to reject the applicant",
                verbose_name="Reject",
            ),
        ),
    ]