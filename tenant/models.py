from django.core.validators import RegexValidator
from django.db import models

# from user.models import User


class Tenant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    created_by = models.IntegerField(default=None, null=True)
