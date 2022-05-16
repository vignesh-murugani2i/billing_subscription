from django.db import models

from service.models import Service


class Plan(models.Model):
    """This class provides model for plan"""

    PLAN_CHOICE = (
        ("1", "Monthly"),
        ("2", "Quarterly"),
        ("3", "Annually")
    )
    name = models.CharField(max_length=250)
    plan_type = models.CharField(choices=PLAN_CHOICE, max_length=1)
    amount = models.IntegerField(default=None)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="plans")
