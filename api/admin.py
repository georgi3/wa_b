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


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'phone', 'address', 'zip_code', 'is_driver', 'is_cook', 'is_server',
                    'is_dishwasher', 'is_photographer', 'last_applied']
    readonly_fields = ['last_applied']
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
    exclude = ['is_withdrawn']

    def has_delete_permission(self, request, obj=None):
        return False


class VolunteerImagesInline(admin.TabularInline):  # or admin.StackedInline
    model = VolunteeringPhotoGallery
    fk_name = 'event'
    extra = 0


@admin.register(VolunteeringEvents)
class VolunteeringEventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'datetime',  'hide_event']
    list_editable = ['hide_event']
    list_per_page = 25
    inlines = [VolunteerAssignmentInline, VolunteerImagesInline]
    actions = [hide_published_events, publish_hidden_events, export_event_volunteers_to_excel,
               export_event_volunteers_to_sheets]
    search_fields = ['title']
    list_filter = [EventDateFilter, EventStatusFilter, 'hide_event']
    ordering = ['datetime']


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
    ordering = ['datetime']
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
