from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

from api.models import AutomatedEmail
from backend.settings import DEFAULT_FROM_EMAIL, MY_APP_DOMAIN, DJANGO_ENV


def custom_social_user(backend, uid, user=None, *args, **kwargs):
    """Makes sure that new user is logged, and not associated with previous login"""
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    user = None
    return {'user': None, 'is_new': user is None, 'new_association': social is None}


def email_as_username(strategy, details, user=None, *args, **kwargs):
    """Makes username be user's email"""
    username = details['email']
    return {'username': username}


def generate_token(strategy, details, response, user=None, *args, **kwargs):
    """Generates token for logged in user"""
    if user:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        strategy.session_set('token', token)
    return {"is_new": user is None}


def user_details(strategy, details, backend, user=None, *args, **kwargs):
    """
    Update user details using data from provider. Customized to update first, last names only if user is new created,
    else protect them.
    """
    if not user:
        return

    changed = False  # flag to track changes

    if strategy.setting("NO_DEFAULT_PROTECTED_USER_FIELDS") is True:
        protected = ()
    else:
        protected = (
            "username",
            "id",
            "pk",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    # Check if the user is newly created based on date_joined
    time_difference = timezone.now() - user.date_joined
    if time_difference < timedelta(minutes=1):
        protected = protected + tuple(strategy.setting("PROTECTED_USER_FIELDS", []))
    else:
        protected = protected + tuple(strategy.setting("PROTECTED_USER_FIELDS", [])) + ("last_name", "first_name")
    field_mapping = strategy.setting("USER_FIELD_MAPPING", {}, backend)
    for name, value in details.items():
        name = field_mapping.get(name, name)
        if value is None or not hasattr(user, name) or name in protected:
            continue

        current_value = getattr(user, name, None)
        if current_value == value:
            continue

        immutable_fields = tuple(strategy.setting("IMMUTABLE_USER_FIELDS", []))
        if name in immutable_fields and current_value:
            continue
        if name == 'first_name' and name not in protected:
            send_google_registration_email(user, value)
        changed = True
        setattr(user, name, value)

    if changed:
        strategy.storage.user.changed(user)


def send_google_registration_email(user, first_name):
    """Sends email to if google registration, avoids regular signal from sending email"""
    try:
        registration_email = AutomatedEmail.objects.get(email_type=AutomatedEmail.REGISTRATION)
        recipient_email = user.email
        send_mail(
            subject=registration_email.email_subject.format(name=first_name),
            message=registration_email.email_content.format(name=first_name),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False
        )
    except ObjectDoesNotExist:
        pass


def redirect_to_complete(strategy, details, user=None, *args, **kwargs):
    token = strategy.session_get('token')
    if strategy.request.session.test_cookie_worked():
        strategy.request.session.delete_test_cookie()
    if DJANGO_ENV == 'development':
        redirect_url = f"http://localhost:3000/login/callback?token={token}"
    else:
        redirect_url = f"https://{MY_APP_DOMAIN}/login/callback?token={token}"
    return redirect(redirect_url)
