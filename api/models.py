from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    community_position = models.CharField("Community Position", max_length=200, default="Volunteer")
    profile_picture = models.ImageField("Profile Image", null=True, blank=True)
    about_me = models.TextField("About Me", null=True, blank=True)
    is_wa_member = models.BooleanField("Is WA Member", default=False)


class VolunteeringEvents(models.Model):
    title = models.CharField("Event Title", max_length=100)
    event_poster = models.ImageField("Event Poster", null=True)
    body = models.TextField("Event Description")
    datetime = models.DateTimeField("Date&Time", help_text="24 hour clock")
    location = models.CharField("Location", max_length=100, default="Berri-UQAM")
    end_time = models.TimeField("Ending Time", help_text="24 hour clock")
    mealsServed = models.IntegerField("Meals Served", blank=True, null=True)
    summary = models.TextField("Event Summary", blank=True, null=True)
    hide_event = models.BooleanField('Hide Event', help_text='Uncheck to display this event.', default=False)
    datetime_created = models.DateTimeField("Created At", auto_now_add=True, null=True)
    datetime_updated = models.DateTimeField("Updated At", auto_now=True, null=True)
    driver_num = models.IntegerField("# of Drivers", default=1)
    cook_num = models.IntegerField("# of Cooks", default=4)
    servers_num = models.IntegerField("# of Servers", default=5)
    dishwashers_num = models.IntegerField("# of Dishwashers", default=1)
    photographers_num = models.IntegerField("# of Photographers", default=1)

    def __str__(self):
        return self.title.title()

    class Meta:
        verbose_name = 'Volunteering Event'
        verbose_name_plural = 'Volunteering Events'

    @property
    def linked_volunteers(self):
        return list(self.assignments.filter(
            confirm_participation=True,
            volunteering_event__datetime__lt=timezone.now()
        ).values_list('volunteer__user_id', flat=True))


class VolunteeringPhotoGallery(models.Model):
    image = models.ImageField("Volunteering Image")
    event = models.ForeignKey(to=VolunteeringEvents, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'VolEvent Image'
        verbose_name_plural = 'VolEvent Images'


class VolunteerManager(models.Manager):
    # def top_users(self):
    #     return User.objects.filter(
    #         volunteer__in=self.annotate(
    #             total_hours=models.Sum('assignments__volunteering_hours')
    #         ).order_by('-total_hours')[:3]
    #     )
    def top_users(self):
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        volunteers_with_hours = User.objects.annotate(
            total_hours=models.Sum(
                'volunteer__assignments__volunteering_hours',
                filter=models.Q(
                    volunteer__assignments__volunteering_event__datetime__gte=thirty_days_ago,
                    volunteer__assignments__volunteering_event__datetime__lte=timezone.now(),
                    volunteer__assignments__confirm_participation=True
                )
            )
        ).filter(total_hours__gt=0).order_by('-total_hours')[:3]
        return volunteers_with_hours


class Volunteer(models.Model):
    objects = VolunteerManager()

    user_id = models.OneToOneField(to=User, on_delete=models.CASCADE, unique=True)
    name = models.CharField("Volunteer's Name", max_length=200, editable=False, null=True)
    email = models.EmailField("Volunteer's Email", editable=False, null=True)
    phone = models.CharField("phone", max_length=12)
    organization = models.CharField("Volunteer's Affiliation", help_text="Organization", max_length=100, blank=True, null=True)
    address = models.CharField("Street Address", max_length=128, blank=True, null=True)
    zip_code = models.CharField("Zip Code", max_length=7, blank=True, null=True)
    car_type = models.CharField("Car Type", max_length=100, blank=True, null=True)
    is_driver = models.BooleanField("Driver", default=False)
    is_cook = models.BooleanField("Cook", default=False)
    is_server = models.BooleanField("Server", default=False)
    is_dishwasher = models.BooleanField("Dishwasher", default=False)
    is_photographer = models.BooleanField("Photographer", default=False)
    joined_date = models.DateTimeField("Joined At", auto_now_add=True, null=True)
    notes = models.TextField("Notes", blank=True, null=True)

    def __str__(self):
        if self.user_id:
            return f"Volunteer {self.user_id.first_name} {self.user_id.last_name}"
        else:
            return "Volunteer (User DNE)"

    @property
    def total_volunteering_hours(self):
        return self.assignments.filter(confirm_participation=True).aggregate(
            total_hours=models.Sum('volunteering_hours'))['total_hours'] or 0
    @property
    def volunteering_hours_last_30(self):
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        total_hours = self.assignments.filter(
            volunteering_event__datetime__gte=thirty_days_ago,
            volunteering_event__datetime__lte=timezone.now(),
            confirm_participation=True
        ).aggregate(
            total_hours=models.Sum('volunteering_hours')
        )['total_hours']
        return total_hours if total_hours is not None else 0

    @property
    def linked_events(self):
        return list(self.assignments.filter(
            confirm_participation=True,
            volunteering_event__datetime__lt=timezone.now()
        ).values_list('volunteering_event', flat=True))

    class Meta:
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'


class VolunteerAssignment(models.Model):
    DRIVER = "Driver"
    COOK = "Cook"
    SERVER = "Server"
    DISHWASHER = "Dishwasher"
    PHOTOGRAPHER = "Photographer"
    VOLUNTEER_CHOICES = [
        (DRIVER, "Driver"),
        (COOK, "Cook"),
        (SERVER, "Server"),
        (DISHWASHER, "Dishwasher"),
        (PHOTOGRAPHER, "Photographer"),
    ]
    volunteering_event = models.ForeignKey(to=VolunteeringEvents, on_delete=models.SET_NULL, null=True,
                                           related_name="assignments")
    assigned_position = models.TextField(max_length=12, choices=VOLUNTEER_CHOICES)
    volunteer = models.ForeignKey(to=Volunteer, on_delete=models.CASCADE, null=True, related_name="assignments")
    approve_participation = models.BooleanField("Approved", help_text="Check to approve participation for the event",
                                                default=False)
    volunteering_hours = models.IntegerField("Actual Volunteering Hours", default=2, blank=True, null=True)
    confirm_participation = models.BooleanField("Participation Confirmed",
                                                help_text="Check to confirm volunteer's participation", default=False)
    is_withdrawn = models.BooleanField("Is Withdrawn", help_text="Applicant Withdrew their application", default=False)
    reject_participation = models.BooleanField("Reject", help_text="Check to reject the applicant", default=False)

    _approve_participation_cache = None
    _confirm_participation_cache = None
    _reject_participation_cache = None
    _withdraw_participation_cache = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._approve_participation_cache = self.approve_participation
        self._confirm_participation_cache = self.confirm_participation
        self._reject_participation_cache = self.reject_participation
        self._withdraw_participation_cache = self.is_withdrawn

    def __str__(self):
        try:
            name = self.volunteer.name.title()
        except Exception as e:
            name = ""
        return f"{self.assigned_position.title()} {name} {self.volunteering_event}"

    def clean(self):
        super().clean()  # call the parent class's clean method

        if self.approve_participation and self.reject_participation:
            raise ValidationError({
                'approve_participation': 'Both approve and reject participation cannot be True at the same time.',
                'reject_participation': 'Both approve and reject participation cannot be True at the same time.',
            })

    class Meta:
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'


class FundraiserEvents(models.Model):
    title = models.CharField("Event Title", max_length=100)
    datetime = models.DateTimeField("Date&Time", help_text="24 hour clock")
    location = models.CharField("Location", max_length=200)
    description = models.TextField("Event Description")
    eventPoster = models.ImageField("Event Poster")
    ticketLink = models.URLField("Link for tickets", help_text="e.g. eventbrite...", blank=True, null=True)
    imgHero = models.ImageField("Hero Image", help_text="Full screen img at the top, choose WIDE img. NOTE: both "
                                                        "'Hero Image' and 'Short Summary' are mandatory for the past"
                                                        " event to be displayed.", blank=True, null=True)
    par1 = models.TextField("Short Summary", help_text="NOTE: both 'Hero Image' and 'Short Summary' are mandatory"
                                                       " for the past event to be displayed.", blank=True, null=True)
    igLink = models.URLField("Instagram Link", blank=True, null=True)
    tiktokLink = models.URLField("TikTok Link", blank=True, null=True)
    fbLink = models.URLField("Facebook Link", blank=True, null=True)
    linkedInLink = models.URLField("LinkedIn Link", blank=True, null=True)
    twitterLink = models.URLField("Twitter Link", blank=True, null=True)
    par2 = models.TextField("First Paragraph", blank=True, null=True)
    par3 = models.TextField("Second Paragraph", blank=True, null=True)
    par4 = models.TextField("Third Paragraph", blank=True, null=True)
    par5 = models.TextField("Fourth Paragraph", blank=True, null=True)
    hide_event = models.BooleanField("Hide Fundraiser", help_text="Uncheck to display this event.", default=False)
    datetime_created = models.DateTimeField("Created At", auto_now_add=True, null=True)
    datetime_updated = models.DateTimeField("Updated At", auto_now=True, null=True)

    def __str__(self):
        return self.title.title()

    class Meta:
        verbose_name = 'Fundraising Event'
        verbose_name_plural = 'Fundraising Events'


class FundraisingPhotoGallery(models.Model):
    image = models.ImageField("Fundraising Image")
    event = models.ForeignKey(to=FundraiserEvents, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Fundraising Image'
        verbose_name_plural = 'Fundraising Images'


class WAGallery(models.Model):
    name = models.CharField("Gallery Name", max_length=120)

    def __str__(self):
        return f"{self.name.title()} Gallery"

    class Meta:
        verbose_name = "WA Gallery"
        verbose_name_plural = "WA Galleries"


class WAPhotos(models.Model):
    image = models.ImageField("Fundraising Image")
    gallery = models.ForeignKey(to=WAGallery, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'


class AutomatedEmail(models.Model):
    # {name}
    # {event}
    # {date}
    # {hours}
    REGISTRATION = "Registration"
    APPLICATION = "Application"
    APPROVAL = "Approval"
    REJECTION = "Rejection"
    WITHDRAWAL = "Withdrawal"
    EVENT_CANCELLATION = "Event_Cancellation"
    CONFIRMATION = "Confirmation"
    FORM_SUBMISSION = "Form_Submission"
    AUTOMATED_EMAIL_CHOICES = [
        (REGISTRATION, "Registration"),
        (APPLICATION, "Application"),
        (APPROVAL, "Approval"),
        (REJECTION, "Rejection"),
        (WITHDRAWAL, "Withdrawal"),
        (EVENT_CANCELLATION, "Event Cancellation"),
        (CONFIRMATION, "Confirmation"),
        (FORM_SUBMISSION, "Form Submission"),
    ]
    email_type = models.TextField("Email Type", max_length=25, choices=AUTOMATED_EMAIL_CHOICES, unique=True)
    email_subject = models.CharField("Email Subject", max_length=200)
    email_content = models.TextField("Email Content")

    def __str__(self):
        return self.email_type

    class Meta:
        verbose_name = 'Automated Email'
        verbose_name_plural = 'Automated Emails'


class ContactForm(models.Model):
    email = models.EmailField("Sender's Email")
    name = models.CharField("Name", max_length=200)
    subject = models.CharField("Email's Subject", max_length=200)
    content = models.TextField("Email's Content")

    class Meta:
        verbose_name = 'Contact Form'
        verbose_name_plural = 'Contact Forms'

    def __str__(self):
        return f"Subject: {self.subject}"
