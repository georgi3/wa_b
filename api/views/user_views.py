from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from api.models import UserProfile, Volunteer, VolunteerAssignment, VolunteeringEvents
from api.serializers.user_serializers import UserSerializer, UserSerializerWithToken, MyTokenObtainPairSerializer, \
    UserAppliedEvents
from api.utilities.views_utilities import is_position_full, apply_volunteer, add_position_to_profile, \
    create_update_fields_dict
from backend.settings import DJANGO_ENV, MY_APP_DOMAIN


class MyTokenObtainPairView(TokenObtainPairView):
    """Log in authentication"""
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data.get("first_name").capitalize(),
            last_name=data.get("last_name").capitalize(),
            username=data.get("email"),
            email=data.get("email"),
            password=make_password(data.get("password"))
        )
        # UserProfile creation is moved to the signal
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except IntegrityError:
        existing_user = User.objects.filter(email=data.get("email")).first()
        if existing_user and not existing_user.password:
            message = {"detail": "Please sign in with Google. User with this email already exists."}
        else:
            message = {"detail": "User with this email already exists."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    user = request.user
    user_serializer = UserSerializerWithToken(user, many=False)
    return Response(user_serializer.data)


@api_view(["GET"])
def get_public_user_profile(request, PK=None):
    user = get_object_or_404(User, id=PK)
    user_serializer = UserSerializer(user, many=False)
    return Response(user_serializer.data)


@api_view(['GET'])
def get_top_volunteers(request):
    top_users = Volunteer.objects.top_users()
    serializer = UserSerializer(top_users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user_id = request.data.get("userId")
    user = User.objects.get(id=user_id)
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(
            user=user,
            community_position="Volunteer",
        )
        userprofile = user.userprofile
    else:
        userprofile = user.userprofile

    profile_picture = request.FILES.get('profile_picture', None)
    about_me = request.data.get('about_me', None)
    if profile_picture:
        # Check if the uploaded file is indeed an image
        if not profile_picture.content_type.startswith('image'):
            return Response({"detail": "Uploaded file is not an image."}, status=status.HTTP_400_BAD_REQUEST)

        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if not any([profile_picture.name.endswith(ext) for ext in allowed_extensions]):
            return Response({"detail": "Image format not supported. Use JPG, JPEG or PNG."},
                            status=status.HTTP_400_BAD_REQUEST)

        if profile_picture.size > 5 * 1024 * 1024:  # 5 MB
            return Response({"detail": "Image is too large. Maximum size is 5 MB."}, status=status.HTTP_400_BAD_REQUEST)

        userprofile.profile_picture = profile_picture
    if about_me:
        # Basic validation for about_me
        if len(about_me.split()) > 70:  # example length check
            return Response({"detail": "About Me is too long."}, status=status.HTTP_400_BAD_REQUEST)
        userprofile.about_me = about_me

    userprofile.save()
    user_serializer = UserSerializerWithToken(user, many=False)
    return Response({**user_serializer.data, **{"detail": "Profile updated successfully"}})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def volunteer_application(request):
    try:
        event_id = int(request.data.get('event_id'))
        user_id = int(request.data.get('user_id'))
        phone = request.data.get('phone')
        organization = request.data.get('organization')
        address = request.data.get('address')
        zip_code = request.data.get('zip_code')
        car_type = request.data.get('car_type')
        vol_position = request.data.get('vol_position')
        update_fields = create_update_fields_dict(phone, organization, car_type, address, zip_code)
        volunteer, _ = Volunteer.objects.update_or_create(
            user_id=User.objects.get(id=user_id),
            defaults=update_fields
        )
        event = get_object_or_404(VolunteeringEvents, pk=event_id)
        add_position_to_profile(position=vol_position, volunteer=volunteer)
        if VolunteerAssignment.objects.filter(volunteering_event=event, volunteer=volunteer,
                                              assigned_position=vol_position).exists():
            return Response({"detail": "You have already applied for this position."},
                            status=status.HTTP_400_BAD_REQUEST)
        position_limits = {
            VolunteerAssignment.DRIVER: event.driver_num,
            VolunteerAssignment.COOK: event.cook_num,
            VolunteerAssignment.SERVER: event.servers_num,
            VolunteerAssignment.DISHWASHER: event.dishwashers_num,
            VolunteerAssignment.PHOTOGRAPHER: event.photographers_num,
        }
        if is_position_full(event, vol_position, position_limits[vol_position]):
            messages = {
                VolunteerAssignment.DRIVER: "Maximum number of drivers has been reached for this event.",
                VolunteerAssignment.COOK: "Maximum number of cooks has been reached for this event.",
                VolunteerAssignment.SERVER: "Maximum number of servers has been reached for this event.",
                VolunteerAssignment.DISHWASHER: "Maximum number of dishwashers has been reached for this event.",
                VolunteerAssignment.PHOTOGRAPHER: "Maximum number of photographers has been reached for this event.",
            }
            return Response({"detail": messages[vol_position]}, status=status.HTTP_400_BAD_REQUEST)
        apply_volunteer(event, vol_position, volunteer)
        return Response({"detail": "Volunteer application successful."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def withdraw_application(request):
    application_id = request.data.get('applicationId')
    if not application_id:
        return Response({"detail": "Application ID is missing."}, status=400)

    try:
        assignment_instance = VolunteerAssignment.objects.get(id=application_id)
        if request.user != assignment_instance.volunteer.user_id:
            return Response({"detail": "You don't have permission to withdraw this application."}, status=403)
        assignment_instance.is_withdrawn = True
        assignment_instance.save()
    except Exception as e:
        return Response({"detail": f"Error Occurred:  {e}"}, status=400)
    return Response({"detail": "Your application has been withdrawn."}, status=202)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_applied_events(request):
    user_id = request.GET.get("userId")
    current_datetime = timezone.now()
    assignments = VolunteerAssignment.objects.filter(
        volunteer__user_id=user_id,
        volunteering_event__datetime__gt=current_datetime
    ).exclude(volunteering_event=None).order_by('volunteering_event__datetime')
    serialized_events = UserAppliedEvents(assignments, many=True)
    return Response(serialized_events.data)


@api_view(["GET"])
def staff_users(request):
    members = User.objects.filter(userprofile__is_wa_member=True)
    serialized_members = UserSerializer(members, many=True)
    return Response(serialized_members.data)


@login_required
def google_login_complete(request):
    token = request.session.get('token')
    # Assuming frontend is served at `http://localhost:3000`
    if DJANGO_ENV == 'development':
        redirect_url = f"http://localhost:3000/login/callback?token={token}"
    else:
        redirect_url = f"https://{MY_APP_DOMAIN}/login/callback?token={token}"

    return HttpResponseRedirect(redirect_url)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_logout(request):
    logout(request)
    request.session.flush()
    return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

