# Generated by Django 4.2.6 on 2024-02-10 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_alter_volunteerassignment_reject_participation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="volunteerassignment",
            old_name="reject_participation",
            new_name="waitlist_participation",
        ),
    ]
