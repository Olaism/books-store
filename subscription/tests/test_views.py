from django.urls import (
    resolve, 
    reverse
)
from django.test import TestCase

from ..views import SubscriptionPlanListView

class SubscriptionPlanViewTest(TestCase):

    def setUp(self):
        url = reverse('sub_plan_list')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/subscription/plan/")
        self.assertEqual(view.func.view_class, SubscriptionPlanListView)