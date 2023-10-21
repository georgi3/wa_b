from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.settings import DEFAULT_FROM_EMAIL
from api.models import WAGallery, ContactForm, AutomatedEmail
from api.serializers.base_serializers import WAGallerySerializer


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
