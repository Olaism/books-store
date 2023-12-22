from django.urls import include, path
from .views import ProfileView

urlpatterns = [
    path("api/", include("users.api.urls")),
    path("", ProfileView.as_view(), name="user_profile"),
]