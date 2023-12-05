from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

User = get_user_model()

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"