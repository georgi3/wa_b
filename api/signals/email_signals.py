from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from api.models import AutomatedEmail, VolunteerAssignment, VolunteeringEvents
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from backend.settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=User)
def registration_email_dispatch(sender, instance, created, **kwargs):
    if created and instance.first_name:
        try:
            registration_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.REGISTRATION)
            name = instance.first_name

            recipient_email = instance.email
            send_mail(
                subject=registration_email.email_subject.format(name=name),
                message=registration_email.email_content.format(name=name),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
        except ObjectDoesNotExist:
            pass


@receiver(post_save, sender=VolunteerAssignment)
def application_email_dispatch(sender, instance, created, **kwargs):
    if created:
        try:
            application_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.APPLICATION)
            name = instance.volunteer.name
            volunteer_position = instance.assigned_position
            event_title = instance.volunteering_event.title
            date = instance.volunteering_event.datetime.strftime('%B %d, %Y')

            recipient_email = instance.volunteer.email
            send_mail(
                subject=application_email.email_subject.format(name=name, volunteer_position=volunteer_position,
                                                               event=event_title, date=date),
                message=application_email.email_content.format(name=name, volunteer_position=volunteer_position,
                                                               event=event_title, date=date),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
        except ObjectDoesNotExist:
            pass


@receiver(post_save, sender=VolunteerAssignment)
def volunteer_assignment_email_dispatch(sender, instance, **kwargs):
    """Dispatches emails for assignment APPROVAL, CONFIRMATION, WAITLIST, WITHDRAWAL"""
    name = instance.volunteer.name
    volunteer_position = instance.assigned_position
    event_title = instance.volunteering_event.title
    date = instance.volunteering_event.datetime.strftime('%B %d, %Y')
    hours = instance.volunteering_hours

    # Check if participation was approved
    if not instance._approve_participation_cache and instance.approve_participation:
        try:
            approval_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.APPROVAL)
            recipient_email = instance.volunteer.email
            send_mail(
                subject=approval_email.email_subject.format(name=name, volunteer_position=volunteer_position,
                                                            event=event_title, date=date),
                message=approval_email.email_content.format(name=name, volunteer_position=volunteer_position,
                                                            event=event_title, date=date),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
        except ObjectDoesNotExist:
            pass

    # Check if participation was confirmed
    if not instance._confirm_participation_cache and instance.confirm_participation:
        try:
            confirmation_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.CONFIRMATION)
            recipient_email = instance.volunteer.email
            send_mail(
                subject=confirmation_email.email_subject.format(name=name, volunteer_position=volunteer_position,
                                                                event=event_title, date=date, hours=hours),
                message=confirmation_email.email_content.format(name=name, volunteer_position=volunteer_position,
                                                                event=event_title, date=date, hours=hours),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
        except ObjectDoesNotExist:
            pass

    # Check if participation was waitlisted
    if not instance._waitlist_participation_cache and instance.waitlist_participation:
        try:
            waitlist_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.WAITLIST)
            recipient_email = instance.volunteer.email
            send_mail(
                subject=waitlist_email.email_subject.format(name=name, volunteer_position=volunteer_position,
                                                            event=event_title, date=date),
                message=waitlist_email.email_content.format(name=name, volunteer_position=volunteer_position,
                                                            event=event_title, date=date),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
            # instance.delete()
        except ObjectDoesNotExist:
            pass

    # Check if participation was withdrawn
    if not instance._withdraw_participation_cache and instance.is_withdrawn:
        try:
            withdrawal_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.WITHDRAWAL)
            recipient_email = instance.volunteer.email
            send_mail(
                subject=withdrawal_email.email_subject.format(name=name, volunteer_position=volunteer_position,
                                                              event=event_title, date=date),
                message=withdrawal_email.email_content.format(name=name, volunteer_position=volunteer_position,
                                                              event=event_title, date=date),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
            if instance.approve_participation == True:
                send_mail(
                    subject=f"IMPORTANT: Volunteer Withdrawal",
                    message=f"Volunteer {name} assigned to be a {volunteer_position} has withdrawn from the "
                            f"{event_title} happening on {date}.",
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[DEFAULT_FROM_EMAIL]
                )
            instance.delete()
        except ObjectDoesNotExist:
            pass

    # Update cached values after checking
    instance._approve_participation_cache = instance.approve_participation
    instance._confirm_participation_cache = instance.confirm_participation
    instance._waitlist_participation_cache = instance.waitlist_participation
    instance._withdraw_participation_cache = instance.is_withdrawn


@receiver(pre_delete, sender=VolunteeringEvents)
def event_cancellation_email_dispatch(sender, instance, **kwargs):
    assignments = VolunteerAssignment.objects.filter(volunteering_event=instance)
    applicants = []
    for assignment in assignments:
        if assignment.volunteer.id in applicants:
            continue
        try:
            cancellation_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.EVENT_CANCELLATION)
            name = assignment.volunteer.name
            event_title = instance.title
            date = instance.datetime.strftime('%B %d, %Y')

            recipient_email = assignment.volunteer.email
            send_mail(
                subject=cancellation_email.email_subject.format(name=name, event=event_title, date=date),
                message=cancellation_email.email_content.format(name=name, event=event_title, date=date),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
        except ObjectDoesNotExist:
            pass
        applicants.append(assignment.volunteer.id)
