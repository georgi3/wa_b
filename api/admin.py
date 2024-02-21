from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, path
from django.contrib import messages
import requests
import json
from django.utils.html import format_html
from django.core.signing import Signer
from .filters import EventDateFilter, EventStatusFilter, CompleteFundraiserFilter
from .models import VolunteeringEvents, FundraiserEvents, UserProfile, Volunteer, VolunteerAssignment, \
    VolunteeringPhotoGallery, FundraisingPhotoGallery, WAGallery, WAPhotos, AutomatedEmail, ContactForm
from .admin_actions import hide_published_events, publish_hidden_events, \
    export_selected_volunteers_to_excel, export_event_volunteers_to_excel, export_event_volunteers_to_sheets, \
    export_selected_volunteers_to_sheets
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from social_django.models import Association, Nonce, UserSocialAuth
import social_django.admin  # NEEDED for the scope to register Association, Nonce, UserSocialAuth to unregister them

admin.site.site_header = "Welfare Avenue"
admin.site.site_title = "Welfare Avenue Admin Portal"
admin.site.index_title = "Welcome to Welfare Avenue Admin Portal"


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Website Users'


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'first_name', 'last_name', "is_staff", 'is_wa_member']
    list_per_page = 25
    list_filter = ["is_staff", "is_superuser", "userprofile__is_wa_member", "groups"]

    def is_wa_member(self, obj):
        is_wa_member = obj.userprofile.is_wa_member
        if is_wa_member:
            return is_wa_member
        return '-'

    is_wa_member.short_description = 'WA Member'


class VolunteerAssignmentBackwardsInline(admin.TabularInline):  # or admin.StackedInline
    model = VolunteerAssignment
    fk_name = 'volunteer'  # ForeignKey field to the Volunteer model
    extra = 0
    exclude = ['is_withdrawn', 'food_drop_off', 'confirmation_message_sent', 'has_confirmed']
    readonly_fields = ['volunteering_event', 'assigned_position', 'approve_participation', 'volunteering_hours',
                       'confirm_participation', 'waitlist_participation', 'event_date']

    def has_delete_permission(self, request, obj=None):
        return False

    def event_date(self, obj):
        return obj.volunteering_event.datetime.date()

    event_date.short_description = 'Date'


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'phone', 'address', 'zip_code', 'is_driver', 'is_cook', 'is_server',
                    'is_dishwasher', 'is_photographer', 'last_applied']
    readonly_fields = ['last_applied']
    inlines = [VolunteerAssignmentBackwardsInline]
    list_per_page = 25
    search_fields = ['name', 'email', 'organization']
    list_filter = ['last_applied', 'joined_date', 'organization', 'is_driver', 'is_cook', 'is_server', 'is_dishwasher',
                   'is_photographer']
    actions = [export_selected_volunteers_to_excel, export_selected_volunteers_to_sheets]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        readonly_fields.extend(['name', 'email'])
        return readonly_fields


class VolunteerAssignmentInline(admin.TabularInline):  # or admin.StackedInline
    model = VolunteerAssignment
    fk_name = 'volunteering_event'  # ForeignKey field to the Volunteer model
    extra = 0
    exclude = ['is_withdrawn', 'confirmation_message_sent', 'has_confirmed']
    readonly_fields = ['details']
    can_delete = True

    def has_delete_permission(self, request, obj=None):
        return True

    def details(self, obj):
        return f"{obj.volunteer.email}\n{obj.volunteer.address}\n{obj.volunteer.zip_code}\n{obj.volunteer.phone}"

    details.short_description = 'Details'


class VolunteerImagesInline(admin.TabularInline):  # or admin.StackedInline
    model = VolunteeringPhotoGallery
    fk_name = 'event'
    extra = 0


@admin.register(VolunteeringEvents)
class VolunteeringEventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'datetime',  'hide_event']  # , 'send_texts_button']
    list_editable = ['hide_event']
    list_per_page = 25
    inlines = [VolunteerAssignmentInline, VolunteerImagesInline]
    actions = [hide_published_events, publish_hidden_events, export_event_volunteers_to_excel,
               export_event_volunteers_to_sheets]
    search_fields = ['title']
    list_filter = [EventDateFilter, EventStatusFilter, 'hide_event']
    ordering = ('-datetime',)

    def send_texts_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Send Texts</a>&nbsp;',
            reverse('admin:send_texts_confirm', args=[obj.pk]),
        )
    send_texts_button.short_description = "Send Texts to Volunteers"
    send_texts_button.allow_tags = True

    # def send_texts(self, request, assignments_ids, message):
    #     selected_assignments = VolunteerAssignment.objects.filter(id__in=assignments_ids)
    #     messages_to_dispatch = list()
    #     for assignment in selected_assignments:
    #         phone = assignment.volunteer.phone
    #         name = assignment.volunteer.name
    #         position = assignment.assigned_position
    #         event_title = assignment.volunteering_event.title
    #         date = assignment.volunteering_event.datetime.date()
    #         messages_to_dispatch.append({
    #             "phone": phone,
    #             "message": message.format(name=name, volunteer_position=position, event=event_title, date=date)
    #         })
    #     print(messages_to_dispatch)
    #     # Perform the sending of text messages here
    #     # Implement your logic to send the messages
    #
    #     self.message_user(request, "Text messages sent successfully.")
    #     return HttpResponseRedirect(reverse('admin:api_volunteeringevents_changelist'))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:event_id>/send_texts_confirm/',
                self.admin_site.admin_view(self.send_texts_confirm),
                name='send_texts_confirm',
            ),
        ]
        return custom_urls + urls

    @staticmethod
    def create_magic_link(request, assignment, signer):
        token = signer.sign(assignment.id)
        magic_link = request.build_absolute_uri(reverse('confirm_participation', args=[token]))
        return f"\nBy clicking this link you confirm your participation: {magic_link}\n\nWarm regards,\n" \
               f"Welfare Avenue Team"

    @staticmethod
    def categorize_assignment(assignment):
        if assignment.assigned_position == 'Cook':
            return 'Cooks'
        elif assignment.assigned_position == 'Server':
            return 'Servers'
        elif assignment.assigned_position == 'Driver':
            return 'Drivers'
        else:
            return 'Others'

    def send_texts_confirm(self, request, event_id):
        if event_id is None:
            self.message_user(request, "No events selected.")
            return HttpResponseRedirect(reverse('admin:api_volunteeringevents_changelist'))

        event = VolunteeringEvents.objects.get(id=event_id)
        assignments = VolunteerAssignment.objects.filter(volunteering_event=event_id)
        grouped_assignments = {
            'Cooks': [],
            'Servers': [],
            'Drivers': [],
            'Others': []
        }
        for assignment in assignments:
            category = self.categorize_assignment(assignment)
            grouped_assignments[category].append(assignment)

        if 'confirm_send' in request.POST:
            selected_assignments = VolunteerAssignment.objects.filter(id__in=request.POST.getlist('assignments'))
            message = request.POST.get('custom_message')
            is_verification_message = bool(request.POST.get('send_magic_link'))
            messages_to_dispatch = list()
            signer = Signer()
            for assignment in selected_assignments:
                """Sending two messages to the same user seem not to work, double check!!!"""
                phone = assignment.volunteer.phone
                name = " ".join(n.capitalize() for n in assignment.volunteer.name.split(" "))
                position = assignment.assigned_position
                event_title = assignment.volunteering_event.title
                date = assignment.volunteering_event.datetime.date()
                magic_link = ''
                if is_verification_message:
                    assignment.waitlist_participation = False
                    assignment.approve_participation = True  # if verification message is sent, it approves application
                    assignment.confirmation_message_sent = True
                    assignment.save()
                    magic_link = self.create_magic_link(request, assignment, signer)
                message = message.format(name=name, volunteer_position=position, event=event_title, date=date)
                messages_to_dispatch.append({
                    "phone": phone,
                    "message": message+magic_link
                })
            data = json.dumps(messages_to_dispatch)
            url = "https://hooks.zapier.com/hooks/catch/10986779/3eooaq7/"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 200:
                self.message_user(request, "Text messages sent successfully.")
            else:
                self.message_user(request, f"Failed to Send Messages: \nStatus Code:{response.status_code}\nHeaders: "
                                           f"{response.headers}\nMessage:{response.json()}", level=messages.ERROR)
            return HttpResponseRedirect(reverse('admin:api_volunteeringevents_changelist'))

        return render(request, 'admin/send_texts_confirm.html', context={
            'event_id': ','.join(event_id),
            'event': event,
            "assignments_grouped": grouped_assignments,
        })

    class Media:
        js = ('js/admin_cook_food_drop_off.js',)


class FundraisingImagesInline(admin.TabularInline):  # or admin.StackedInline
    model = FundraisingPhotoGallery
    fk_name = 'event'
    extra = 0


@admin.register(FundraiserEvents)
class FundraiserEventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'datetime', 'hide_event']
    list_editable = ['hide_event']
    list_per_page = 25
    inlines = [FundraisingImagesInline]
    actions = [hide_published_events, publish_hidden_events]
    ordering = ('-datetime', )
    list_filter = [CompleteFundraiserFilter, 'hide_event']


class WAPhotosInline(admin.TabularInline):  # or admin.StackedInline
    model = WAPhotos
    fk_name = 'gallery'
    extra = 0


@admin.register(WAGallery)
class WAGallery(admin.ModelAdmin):
    inlines = [WAPhotosInline]


@admin.register(AutomatedEmail)
class AutomatedEmailAdmin(admin.ModelAdmin):
    list_display = ["email_type"]


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    readonly_fields = ["email", "name", "subject", "content"]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Unregister django social Nonce, Association, UserSocialAuth
try:
    admin.site.unregister(Association)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Nonce)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(UserSocialAuth)
except admin.sites.NotRegistered:
    pass
