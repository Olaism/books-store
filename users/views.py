from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

User = get_user_model()

class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ("first_name", "last_name", "username", "profile_photo")
    template_name = "users/profile.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self):
        return self.request.user