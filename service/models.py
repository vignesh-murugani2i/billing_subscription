from django.db import models


class Service(models.Model):
    """This class provides model for plan"""

    name = models.CharField(max_length=250)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
