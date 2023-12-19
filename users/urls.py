from django.urls import include, path

from .views import ProfileView

urlpatterns = [
    path("api/", include("dj_rest_auth.urls")),
    path("api/registration/", include("dj_rest_auth.registration.urls")),
    path("", ProfileView.as_view(), name="user_profile"),
]