"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import user_views as api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls.base_urls")),
    path("api/users/", include("api.urls.users_urls")),
    path("api/events/", include("api.urls.events_urls")),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('accounts/login/google-oauth2/complete/', api_views.google_login_complete, name='google-login-complete'),
    path('accounts/logout/', api_views.google_logout, name='google-logout'),
    path('api/auth/', include('djoser.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)