from django.urls import path
from api.views import user_views as views


urlpatterns = [
    path("login", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('apply', views.volunteer_application, name='apply'),
    path('withdraw', views.withdraw_application, name='withdraw'),
    path("register", views.register_user, name="register"),
    path("profile", views.get_my_profile, name="my_profile"),
    path("profile/applied-events", views.get_applied_events, name="get_applied_events"),
    path("profile/update", views.update_user_profile, name="update_profile"),
    path("profile/<int:PK>/", views.get_public_user_profile, name="user_profile"),
    path("top-volunteers", views.get_top_volunteers, name="top_volunteers"),
    path("staff-members", views.staff_users, name="team_members"),
]


