from django.db import models

from card.models import Card
from plan.models import Plan
from service.models import Service
from tenant.models import Tenant
from user.models import User


class Subscription(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="subscriptions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="subscriptions")
    remind_days = models.IntegerField(default=2)
    account_mail = models.EmailField()
    start_subscription_date = models.DateField()
    cycle_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    is_active = models.BooleanField(default=True)
    next_subscription_date = models.DateField(null=True)
    subscription_end_date = models.DateField(null=True)
    remind_date = models.DateField(null=True)
