from django.urls import path
from api.views import event_views as views


urlpatterns = [
    path("all/", views.get_all_events, name="all_events"),
    path("volunteering/", views.get_volunteering_events, name="volunteering_events"),
    path('volunteering/filter', views.filter_volunteering_events, name='filter_events'),
    path("volunteering/<str:PK>", views.get_volunteering_event, name="volunteering_event"),
    path("fundraising/", views.get_fundraiser_events, name="fundraising_events"),
    path("fundraising/<str:PK>", views.get_fundraiser_event, name="fundraising_event"),
]
