from django.urls import include, path

from .views import CustomPasswordResetConfirmView

urlpatterns = [
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("password/reset/confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("", include("dj_rest_auth.urls")),
]