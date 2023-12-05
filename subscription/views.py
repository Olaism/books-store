from django.views.generic import ListView

from .models import SubscriptionPlan

class SubscriptionPlanListView(ListView):
    model = SubscriptionPlan
    template_name = 'subscription/list.html'
    context_object_name = 'subscription_plans'