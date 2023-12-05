from django.urls import path

from .views import SubscriptionPlanListView

urlpatterns = [
    path("plan/", SubscriptionPlanListView.as_view(), name='sub_plan_list'),
]