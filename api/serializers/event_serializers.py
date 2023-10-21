from rest_framework import serializers
from api.models import VolunteeringEvents, FundraiserEvents, VolunteeringPhotoGallery, \
    FundraisingPhotoGallery, VolunteerAssignment
from api.serializers.user_serializers import UserWithPositionSerializer


class VolunteeringPhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringPhotoGallery
        fields = ["image"]


class VolunteeringEventsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VolunteeringEvents
        fields = ["id", "title", "event_poster", "body", "datetime", "location", "end_time", "mealsServed", "summary",
                  "hide_event", "datetime_created", "datetime_updated", "driver_num", "cook_num", "servers_num",
                  "dishwashers_num", "photographers_num", "images"]

    def get_images(self, obj):
        images = VolunteeringPhotoGallery.objects.filter(event=obj.id)
        return VolunteeringPhotoGallerySerializer(images, many=True).data


class VolunteeringEventSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    linked_volunteers = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VolunteeringEvents
        fields = ["id", "title", "event_poster", "body", "datetime", "location", "end_time", "mealsServed", "summary",
                  "hide_event", "datetime_created", "datetime_updated", "driver_num", "cook_num", "servers_num",
                  "dishwashers_num", "photographers_num", "images", "linked_volunteers"]

    def get_images(self, obj):
        images = VolunteeringPhotoGallery.objects.filter(event=obj.id)
        return VolunteeringPhotoGallerySerializer(images, many=True).data

    def get_linked_volunteers(self, obj):
        volunteer_assignments = VolunteerAssignment.objects.filter(
            volunteering_event=obj,
            confirm_participation=True,
            volunteer__user_id__isnull=False
        ).select_related('volunteer__user_id').prefetch_related('volunteer')

        volunteers_with_positions = [
            {
                **UserWithPositionSerializer(
                    volunteer.volunteer.user_id,
                    context={'event': obj, 'assignments': {assignment.volunteer_id: assignment for assignment in
                                                           volunteer_assignments}}
                ).data,
                "assigned_position": volunteer.assigned_position
            }
            for volunteer in volunteer_assignments
        ]
        return volunteers_with_positions


class FundraisingPhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundraisingPhotoGallery
        fields = ["image"]


class FundraiserEventsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FundraiserEvents
        fields = ["id", "title", "datetime", "location", "description", "eventPoster", "ticketLink", "imgHero", "par1",
                  "igLink", "tiktokLink", "fbLink", "linkedInLink", "twitterLink", "par2", "par3", "par4", "par5",
                  "hide_event", "datetime_created", "datetime_updated", "images"
                  ]

    def get_images(self, obj):
        images = FundraisingPhotoGallery.objects.filter(event=obj.id)
        return FundraisingPhotoGallerySerializer(images, many=True).data