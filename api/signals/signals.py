from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from api.models import Volunteer, UserProfile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, community_position="Volunteer")


# TODO if volunteer is assigned to event check True position for the volunteer

def update_user(sender, instance, **kwargs):
    user = instance
    if user.email != "":
        user.username = user.email


@receiver(pre_save, sender=Volunteer)
def update_volunteer_fields(sender, instance, **kwargs):
    if instance.user_id:
        # Update the name and email fields based on the related user's data
        instance.name = f"{instance.user_id.first_name} {instance.user_id.last_name}"
        instance.email = instance.user_id.email


pre_save.connect(update_user, sender=User)
pre_save.connect(update_volunteer_fields, sender=Volunteer)
