import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.http import HttpResponseRedirect
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.settings import DEFAULT_FROM_EMAIL, DJANGO_ENV, MY_APP_DOMAIN
from api.models import WAGallery, ContactForm, AutomatedEmail, VolunteerAssignment
from api.serializers.base_serializers import WAGallerySerializer
from django.shortcuts import render, get_object_or_404, redirect


@api_view(["GET"])
def get_wa_galleries(request):
    galleries = WAGallery.objects.all()
    galleries_serializer = WAGallerySerializer(galleries, many=True)
    return Response(galleries_serializer.data)


@api_view(['POST'])
def submit_contact_form(request):
    form_submission_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.FORM_SUBMISSION)
    try:
        email = request.data.get("email")
        name = request.data.get("name")
        subject = request.data.get("subject")
        content = request.data.get("content")
        ContactForm.objects.create(
            email=email,
            name=name,
            subject=subject,
            content=content
        )
        # send note to sender
        send_mail(
            subject=subject,
            message=content,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[DEFAULT_FROM_EMAIL],
            fail_silently=False
        )
        # send email to us
        send_mail(
            subject=form_submission_email.email_subject.format(name=name),
            message=form_submission_email.email_content.format(name=name),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Thank you for contacting us, we will get back to you shortly."})


@api_view(["POST"])
def confirm_participation(request):
    signer = TimestampSigner()
    try:
        token = json.loads(request.body).get('token')
        assignment_id = signer.unsign(token, max_age=timedelta(hours=24))
        with transaction.atomic():
            # Lock the assignment row until the end of the transaction block
            assignment = VolunteerAssignment.objects.select_for_update().get(id=assignment_id)
            if assignment.has_confirmed:
                return Response({'status': 'success', 'message': 'Participation has already been confirmed.'})

            assignment.has_confirmed = True
            assignment.save()
            return Response({'status': 'success', 'message': 'Participation confirmed'})

    except SignatureExpired:
        return Response({'status': 'error', 'message': 'Link has expired, please reach out to our team.'}, status=410)
    except BadSignature:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=400)
