from django.db import models

from subscription.models import Subscription
from tenant.models import Tenant


class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="subscriptions")
    amount = models.IntegerField()
    payment_date = models.DateTimeField()
    is_payment_success = models.BooleanField()
