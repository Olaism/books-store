import secrets
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    days = models.PositiveIntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


class Subscription(models.Model):
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    user = models.OneToOneField(User, 
        related_name='subscription',
        on_delete=models.CASCADE)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()
    ref = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return self.date_ended >= timezone.now()

    def __str__(self):
        return f"{self.user.email} subscribed till {self.date_ended}"

    def save(self, *args, **kwargs):
        self.date_ended = self.date_started \
                     + timezone.timedelta(days=self.subscription_plan.days)
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Subscription.objects.get(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        return super().save(*args, **kwargs)