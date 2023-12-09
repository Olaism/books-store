import secrets
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from ..models import (
    Subscription,
    SubscriptionPlan
)

User = get_user_model()

class SubscriptionPlanDefaultCaseTest(TestCase):
    
    def test_subplan_listing(self):
        sub_plan = SubscriptionPlan.objects.create(
            sub_type="BS",
            name="basic - 1 month",
            price=1000.00,
        )
        self.assertEqual(sub_plan.sub_type, "BS")
        self.assertEqual(sub_plan.name, "basic - 1 month")
        self.assertEqual(sub_plan.price, 1000.00)
        self.assertEqual(sub_plan.days, 30) # use default
        self.assertEqual(sub_plan.slug, "basic-1-month") # use default
        self.assertEqual(str(sub_plan), "basic - 1 month") # test __str__ method

class SubscriptionPlanTest(TestCase):

    def test_subplan_listing(self):
        sub_plan = SubscriptionPlan.objects.create(
            sub_type="PR",
            name="premium - 6 months",
            price=1000.99,
            days=180
        )
        self.assertEqual(sub_plan.sub_type, "PR")
        self.assertEqual(sub_plan.name, "premium - 6 months")
        self.assertEqual(sub_plan.price, 1000.99)
        self.assertEqual(sub_plan.days, 180)
        self.assertEqual(sub_plan.slug, "premium-6-months") # use default

class SubscriptionDefaultCaseTest(TestCase):

    def setUp(self):
        self.get_date_time = timezone.now()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="testpassword"
        )
        self.plan = SubscriptionPlan.objects.create(
            sub_type="BS",
            name="basic",
            price=1200.00
        )
        self.default_sub = Subscription.objects.create(
            subscription_plan=self.plan,
            user = self.user,
        )
    def test_subscription_listing(self):
        self.assertEqual(self.default_sub.subscription_plan, self.plan)
        self.assertEqual(self.default_sub.user, self.user)
        self.assertEqual(
            self.default_sub.date_ended,
            self.default_sub.date_started+timezone.timedelta(days=self.plan.days))
        self.assertFalse(self.default_sub.verified)
        self.assertTrue(self.default_sub.is_active) # property added

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
            sub_type="BS",
            name="basic",
            price=1200.00
        )
        self.sub = Subscription.objects.create(
            subscription_plan=self.plan,
            user = self.user,
            date_started=self.get_date_time,
            ref=self.ref,
            date_ended= self.get_date_time + \
                timezone.timedelta(days=self.plan.days),
            verified=True
        )

    def test_subscription_listing(self):
        self.assertEqual(self.sub.subscription_plan, self.plan)
        self.assertEqual(self.sub.user, self.user)
        self.assertEqual(self.sub.date_started, self.get_date_time)
        self.assertEqual(
            self.sub.date_ended, 
            self.get_date_time + timezone.timedelta(days=self.plan.days))
        self.assertEqual(self.sub.ref, self.ref)
        self.assertTrue(self.sub.verified)
        self.assertTrue(self.sub.is_active) # property added