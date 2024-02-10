# Generated by Django 4.2.6 on 2024-02-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_volunteerassignment_food_drop_off"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volunteerassignment",
            name="food_drop_off",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="Cook will drop off the food",
                null=True,
                verbose_name="Food Is Dropped Off",
            ),
        ),
    ]
