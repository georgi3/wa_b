from rest_framework import serializers
from api.models import Volunteer, VolunteerAssignment
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("Given credentials are incorrect. Please try again.")
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        # data = dict()
        # data['email'] = self.user.email
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            # data['username'] = self.user.username
            data[k] = v
        return data


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    about_me = serializers.SerializerMethodField(read_only=True)
    profile_picture = serializers.SerializerMethodField(read_only=True)
    community_position = serializers.SerializerMethodField(read_only=True)
    total_volunteering_hours = serializers.SerializerMethodField(read_only=True)
    linked_events = serializers.SerializerMethodField(read_only=True)
    is_wa_member = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",  "name", "about_me", "community_position", "profile_picture",
                  "total_volunteering_hours", "linked_events", "is_wa_member"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_about_me(self, obj):
        try:
            data = obj.userprofile.about_me
        except ObjectDoesNotExist:
            data = ""
        return data

    def get_profile_picture(self, obj):
        try:
            data = obj.userprofile.profile_picture.url
        except Exception as e:
            data = None
        return data

    def get_community_position(self, obj):
        try:
            data = obj.userprofile.community_position
        except ObjectDoesNotExist:
            data = "DNE"
        return data

    def get_is_wa_member(self, obj):
        try:
            is_member = obj.userprofile.is_wa_member
        except Exception as e:
            is_member = False
        return is_member

    def get_total_volunteering_hours(self, obj):
        try:
            volunteer = Volunteer.objects.get(user_id=obj.id)
            return volunteer.total_volunteering_hours
        except Volunteer.DoesNotExist:
            return 0

    def get_linked_events(self, obj):
        try:
            volunteer = Volunteer.objects.get(user_id=obj.id)
            return volunteer.linked_events
        except Volunteer.DoesNotExist:
            return []


class UserWithPositionSerializer(UserSerializer):
    assigned_position = serializers.CharField(source="get_assigned_position", read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['assigned_position']

    def get_assigned_position(self, obj):
        assignments = self.context.get('assignments', {})
        assignment = assignments.get(obj.id)
        return assignment.assigned_position if assignment else None


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    phone = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    car_type = serializers.SerializerMethodField(read_only=True)
    zip_code = serializers.SerializerMethodField(read_only=True)
    organization = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "token", "phone", "address", "car_type",
                  "zip_code", "organization", "community_position", "profile_picture", "about_me",
                  "total_volunteering_hours", "linked_events", "is_wa_member"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_phone(self, obj):
        try:
            return obj.volunteer.phone
        except Volunteer.DoesNotExist:
            return None

    def get_address(self, obj):
        try:
            return obj.volunteer.address
        except Volunteer.DoesNotExist:
            return None

    def get_car_type(self, obj):
        try:
            return obj.volunteer.car_type
        except Volunteer.DoesNotExist:
            return None

    def get_zip_code(self, obj):
        try:
            return obj.volunteer.zip_code
        except Volunteer.DoesNotExist:
            return None

    def get_organization(self, obj):
        try:
            return obj.volunteer.organization
        except Volunteer.DoesNotExist:
            return None


class UserAppliedEvents(serializers.Serializer):
    title = serializers.SerializerMethodField(read_only=True)
    volunteering_event_id = serializers.SerializerMethodField(read_only=True)
    approved_participation = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    assigned_position = serializers.SerializerMethodField(read_only=True)
    assignment_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VolunteerAssignment
        fields = ["assignment_id", "assigned_position", "title", "volunteering_event_id", "approved_participation", "date"]

    def get_assignment_id(self, obj):
        return obj.id

    def get_title(self, obj):
        try:
            title = obj.volunteering_event.title
            return title
        except AttributeError as e:
            pass

    def get_volunteering_event_id(self, obj):
        try:
            return obj.volunteering_event.id
        except AttributeError as e:
            pass

    def get_date(self, obj):
        try:
            return obj.volunteering_event.datetime
        except AttributeError as e:
            pass

    def get_approved_participation(self, obj):
        return obj.approve_participation

    def get_assigned_position(self, obj):
        return obj.assigned_position
