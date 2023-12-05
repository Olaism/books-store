import secrets
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from ..models import (
    Subscription,
    SubscriptionPlan
)

User = get_user_model()

class SubscriptionPlanTest(TestCase):
    
    def test_subplan_listing(self):
        sub_plan = SubscriptionPlan.objects.create(
            name="basic",
            price=1000.00,
        )
        self.assertEqual(sub_plan.name, "basic")
        self.assertEqual(sub_plan.price, 1000.00)
        self.assertEqual(sub_plan.days, 30)
        self.assertEqual(sub_plan.slug, "basic")

class SubscriptionTest(TestCase):

    def setUp(self):
        self.get_date_time = timezone.now()
        self.ref = secrets.token_urlsafe(50)
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="testpassword"
        )
        self.plan = SubscriptionPlan.objects.create(
            name="basic",
            price=1200.00
        )
        self.pub = Subscription.objects.create(
            subscription_plan=self.plan,
            user = self.user,
            date_started=self.get_date_time,
            ref=self.ref
        )

    def test_subscription_listing(self):
        self.assertEqual(self.pub.subscription_plan, self.plan)
        self.assertEqual(self.pub.user, self.user)
        self.assertEqual(self.pub.date_started, self.get_date_time)
        self.assertEqual(
            self.pub.date_ended, 
            self.get_date_time + timezone.timedelta(days=self.plan.days))
        self.assertEqual(self.pub.ref, self.ref)
        self.assertTrue(self.pub.is_active)