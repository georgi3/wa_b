# Generated by Django 4.2.6 on 2023-10-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_volunteerassignment_is_withdrawn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volunteeringevents",
            name="cook_num",
            field=models.IntegerField(default=4, verbose_name="# of Cooks"),
        ),
        migrations.AlterField(
            model_name="volunteeringevents",
            name="dishwashers_num",
            field=models.IntegerField(default=1, verbose_name="# of Dishwashers"),
        ),
        migrations.AlterField(
            model_name="volunteeringevents",
            name="driver_num",
            field=models.IntegerField(default=1, verbose_name="# of Drivers"),
        ),
        migrations.AlterField(
            model_name="volunteeringevents",
            name="photographers_num",
            field=models.IntegerField(default=1, verbose_name="# of Photographers"),
        ),
        migrations.AlterField(
            model_name="volunteeringevents",
            name="servers_num",
            field=models.IntegerField(default=5, verbose_name="# of Servers"),
        ),
    ]
