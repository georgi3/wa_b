# Generated by Django 4.2.6 on 2023-10-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_alter_volunteeringevents_cook_num_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="automatedemail",
            name="email_type",
            field=models.TextField(
                choices=[
                    ("Registration", "Registration"),
                    ("Application", "Application"),
                    ("Approval", "Approval"),
                    ("Rejection", "Rejection"),
                    ("Withdrawal", "Withdrawal"),
                    ("Event_Cancellation", "Event Cancellation"),
                    ("Confirmation", "Confirmation"),
                    ("Form_Submission", "Form Submission"),
                ],
                max_length=25,
                unique=True,
                verbose_name="Email Type",
            ),
        ),
    ]