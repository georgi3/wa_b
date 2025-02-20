# Generated by Django 4.2.19 on 2025-02-20 22:15

from django.db import migrations, models
from django.utils import timezone

def update_attended(apps, schema_editor):
    VolunteerAssignment = apps.get_model('api', 'VolunteerAssignment')
    now = timezone.now()

    for obj in VolunteerAssignment.objects.select_related('volunteering_event').all():
        if obj.volunteering_event:
            if obj.volunteering_event.datetime < now:
                obj.attended = True
                obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ("api", "0024_alter_volunteerassignment_confirm_participation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volunteerassignment",
            name="attended",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Attended"
            ),
        ),
        migrations.RunPython(update_attended),
    ]
