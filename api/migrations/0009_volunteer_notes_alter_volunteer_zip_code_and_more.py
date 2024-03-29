# Generated by Django 4.2.6 on 2023-11-09 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_alter_automatedemail_email_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteer",
            name="notes",
            field=models.TextField(blank=True, null=True, verbose_name="Notes"),
        ),
        migrations.AlterField(
            model_name="volunteer",
            name="zip_code",
            field=models.CharField(
                blank=True, max_length=7, null=True, verbose_name="Zip Code"
            ),
        ),
        migrations.AlterField(
            model_name="volunteeringevents",
            name="location",
            field=models.CharField(
                default="Berri-UQAM", max_length=100, verbose_name="Location"
            ),
        ),
    ]
