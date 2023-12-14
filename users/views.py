from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from subscription.models import Subscription

User = get_user_model()

class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ("first_name", "last_name", "username", "profile_photo")
    template_name = "users/profile.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        try:
            sub = Subscription.objects.get(user=self.request.user)
        except Subscription.DoesNotExist:
            context["is_subscribed"] = False
            return context

        context["is_subscribed"] = True

        return context