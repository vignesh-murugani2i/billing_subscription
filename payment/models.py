from django.db import models

from subscription.models import Subscription
from tenant.models import Tenant
from user.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="subscriptions")
    amount = models.IntegerField()
    payment_date = models.DateTimeField()
    is_payment_success = models.BooleanField()
