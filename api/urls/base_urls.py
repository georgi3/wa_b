from django.urls import path
from api.views import base_views


urlpatterns = [
    path("content/galleries", base_views.get_wa_galleries, name="galleries"),
    path("contact-form-submission", base_views.submit_contact_form, name='contact-form-submission'),
    path('confirm/<str:token>/', base_views.confirm_participation, name='confirm_participation')
]
