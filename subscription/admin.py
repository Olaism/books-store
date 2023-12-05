from django.contrib import admin

from .models import (
    Subscription,
    SubscriptionPlan
)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "subscription_plan", 
                    "date_started", "date_ended", "ref", "verified")
    list_filter = ("date_started", "date_ended",)