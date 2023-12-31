# Generated by Django 4.2.6 on 2023-10-09 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AutomatedEmail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email_type",
                    models.TextField(
                        choices=[
                            ("Registration", "Registration"),
                            ("Application", "Application"),
                            ("Approval", "Approval"),
                            ("Rejection", "Rejection"),
                            ("User_Cancellation", "User Cancellation"),
                            ("Organization_Cancellation", "Organization Cancellation"),
                            ("Confirmation", "Confirmation"),
                            ("Form_Submission", "Form Submission"),
                        ],
                        max_length=25,
                        unique=True,
                        verbose_name="Email Type",
                    ),
                ),
                (
                    "email_subject",
                    models.CharField(max_length=200, verbose_name="Email Subject"),
                ),
                ("email_content", models.TextField(verbose_name="Email Content")),
            ],
            options={
                "verbose_name": "Automated Email",
                "verbose_name_plural": "Automated Emails",
            },
        ),
        migrations.CreateModel(
            name="FundraiserEvents",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Event Title")),
                (
                    "datetime",
                    models.DateTimeField(
                        help_text="24 hour clock", verbose_name="Date&Time"
                    ),
                ),
                ("location", models.CharField(max_length=200, verbose_name="Location")),
                ("description", models.TextField(verbose_name="Event Description")),
                (
                    "eventPoster",
                    models.ImageField(upload_to="", verbose_name="Event Poster"),
                ),
                (
                    "ticketLink",
                    models.URLField(
                        blank=True,
                        help_text="e.g. eventbrite...",
                        null=True,
                        verbose_name="Link for tickets",
                    ),
                ),
                (
                    "imgHero",
                    models.ImageField(
                        blank=True,
                        help_text="Full screen img at the top, choose WIDE img. NOTE: both 'Hero Image' and 'Short Summary' are mandatory for the past event to be displayed.",
                        null=True,
                        upload_to="",
                        verbose_name="Hero Image",
                    ),
                ),
                (
                    "par1",
                    models.TextField(
                        blank=True,
                        help_text="NOTE: both 'Hero Image' and 'Short Summary' are mandatory for the past event to be displayed.",
                        null=True,
                        verbose_name="Short Summary",
                    ),
                ),
                (
                    "igLink",
                    models.URLField(
                        blank=True, null=True, verbose_name="Instagram Link"
                    ),
                ),
                (
                    "tiktokLink",
                    models.URLField(blank=True, null=True, verbose_name="TikTok Link"),
                ),
                (
                    "fbLink",
                    models.URLField(
                        blank=True, null=True, verbose_name="Facebook Link"
                    ),
                ),
                (
                    "linkedInLink",
                    models.URLField(
                        blank=True, null=True, verbose_name="LinkedIn Link"
                    ),
                ),
                (
                    "twitterLink",
                    models.URLField(blank=True, null=True, verbose_name="Twitter Link"),
                ),
                (
                    "par2",
                    models.TextField(
                        blank=True, null=True, verbose_name="First Paragraph"
                    ),
                ),
                (
                    "par3",
                    models.TextField(
                        blank=True, null=True, verbose_name="Second Paragraph"
                    ),
                ),
                (
                    "par4",
                    models.TextField(
                        blank=True, null=True, verbose_name="Third Paragraph"
                    ),
                ),
                (
                    "par5",
                    models.TextField(
                        blank=True, null=True, verbose_name="Fourth Paragraph"
                    ),
                ),
                (
                    "hide_event",
                    models.BooleanField(
                        default=False,
                        help_text="Uncheck to display this event.",
                        verbose_name="Hide Fundraiser",
                    ),
                ),
                (
                    "datetime_created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created At"
                    ),
                ),
                (
                    "datetime_updated",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated At"
                    ),
                ),
            ],
            options={
                "verbose_name": "Fundraising Event",
                "verbose_name_plural": "Fundraising Events",
            },
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        editable=False,
                        max_length=200,
                        null=True,
                        verbose_name="Volunteer's Name",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        editable=False,
                        max_length=254,
                        null=True,
                        verbose_name="Volunteer's Email",
                    ),
                ),
                ("phone", models.CharField(max_length=12, verbose_name="phone")),
                (
                    "organization",
                    models.CharField(
                        blank=True,
                        help_text="Organization",
                        max_length=100,
                        null=True,
                        verbose_name="Volunteer's Affiliation",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        max_length=128,
                        null=True,
                        verbose_name="Street Address",
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(
                        blank=True, max_length=6, null=True, verbose_name="Zip Code"
                    ),
                ),
                (
                    "car_type",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Car Type"
                    ),
                ),
                (
                    "is_driver",
                    models.BooleanField(default=False, verbose_name="Driver"),
                ),
                ("is_cook", models.BooleanField(default=False, verbose_name="Cook")),
                (
                    "is_server",
                    models.BooleanField(default=False, verbose_name="Server"),
                ),
                (
                    "is_dishwasher",
                    models.BooleanField(default=False, verbose_name="Dishwasher"),
                ),
                (
                    "is_photographer",
                    models.BooleanField(default=False, verbose_name="Photographer"),
                ),
                (
                    "joined_date",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Joined At"
                    ),
                ),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Volunteer",
                "verbose_name_plural": "Volunteers",
            },
        ),
        migrations.CreateModel(
            name="VolunteeringEvents",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Event Title")),
                (
                    "event_poster",
                    models.ImageField(
                        null=True, upload_to="", verbose_name="Event Poster"
                    ),
                ),
                ("body", models.TextField(verbose_name="Event Description")),
                (
                    "datetime",
                    models.DateTimeField(
                        help_text="24 hour clock", verbose_name="Date&Time"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        default="Beri UQAM", max_length=100, verbose_name="Location"
                    ),
                ),
                (
                    "end_time",
                    models.TimeField(
                        help_text="24 hour clock", verbose_name="Ending Time"
                    ),
                ),
                (
                    "mealsServed",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Meals Served"
                    ),
                ),
                (
                    "summary",
                    models.TextField(
                        blank=True, null=True, verbose_name="Event Summary"
                    ),
                ),
                (
                    "hide_event",
                    models.BooleanField(
                        default=False,
                        help_text="Uncheck to display this event.",
                        verbose_name="Hide Event",
                    ),
                ),
                (
                    "datetime_created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created At"
                    ),
                ),
                (
                    "datetime_updated",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated At"
                    ),
                ),
                (
                    "driver_num",
                    models.IntegerField(default=1, verbose_name="Number of Drivers"),
                ),
                (
                    "cook_num",
                    models.IntegerField(default=4, verbose_name="Number of Cooks"),
                ),
                (
                    "servers_num",
                    models.IntegerField(default=5, verbose_name="Number of Servers"),
                ),
                (
                    "dishwashers_num",
                    models.IntegerField(
                        default=1, verbose_name="Number of Dishwashers"
                    ),
                ),
                (
                    "photographers_num",
                    models.IntegerField(
                        default=1, verbose_name="Number of Photographers"
                    ),
                ),
            ],
            options={
                "verbose_name": "Volunteering Event",
                "verbose_name_plural": "Volunteering Events",
            },
        ),
        migrations.CreateModel(
            name="WAGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="Gallery Name")),
            ],
            options={
                "verbose_name": "WA Gallery",
                "verbose_name_plural": "WA Galleries",
            },
        ),
        migrations.CreateModel(
            name="WAPhotos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="", verbose_name="Fundraising Image"),
                ),
                (
                    "gallery",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.wagallery"
                    ),
                ),
            ],
            options={
                "verbose_name": "Gallery Image",
                "verbose_name_plural": "Gallery Images",
            },
        ),
        migrations.CreateModel(
            name="VolunteeringPhotoGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="", verbose_name="Volunteering Image"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.volunteeringevents",
                    ),
                ),
            ],
            options={
                "verbose_name": "VolEvent Image",
                "verbose_name_plural": "VolEvent Images",
            },
        ),
        migrations.CreateModel(
            name="VolunteerAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assigned_position",
                    models.TextField(
                        choices=[
                            ("Driver", "Driver"),
                            ("Cook", "Cook"),
                            ("Server", "Server"),
                            ("Dishwasher", "Dishwasher"),
                            ("Photographer", "Photographer"),
                        ],
                        max_length=12,
                    ),
                ),
                (
                    "approve_participation",
                    models.BooleanField(
                        default=False,
                        help_text="Check to approve participation for the event",
                        verbose_name="Approved",
                    ),
                ),
                (
                    "confirm_participation",
                    models.BooleanField(
                        default=False,
                        help_text="Check to confirm volunteer's participation",
                        verbose_name="Participation Confirmed",
                    ),
                ),
                (
                    "volunteering_hours",
                    models.IntegerField(
                        blank=True,
                        default=2,
                        null=True,
                        verbose_name="Actual Volunteering Hours",
                    ),
                ),
                (
                    "volunteer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to="api.volunteer",
                    ),
                ),
                (
                    "volunteering_event",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assignments",
                        to="api.volunteeringevents",
                    ),
                ),
            ],
            options={
                "verbose_name": "Volunteer",
                "verbose_name_plural": "Volunteers",
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "community_position",
                    models.CharField(
                        default="Volunteer",
                        max_length=200,
                        verbose_name="Community Position",
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="Profile Image",
                    ),
                ),
                (
                    "about_me",
                    models.TextField(blank=True, null=True, verbose_name="About Me"),
                ),
                (
                    "is_wa_member",
                    models.BooleanField(default=False, verbose_name="Is WA Member"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FundraisingPhotoGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="", verbose_name="Fundraising Image"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.fundraiserevents",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fundraising Image",
                "verbose_name_plural": "Fundraising Images",
            },
        ),
    ]
