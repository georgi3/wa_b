# Generated by Django 4.2.6 on 2024-02-10 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_alter_automatedemail_email_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerassignment",
            name="food_drop_off",
            field=models.BooleanField(
                blank=True,
                help_text="Cook will drop off the food",
                null=True,
                verbose_name="Food Is Dropped Off",
            ),
        ),
    ]
