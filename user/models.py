from django.core.validators import RegexValidator
from django.db import models

from tenant.models import Tenant


class User(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.BigIntegerField(validators=[
        RegexValidator(
            regex='^[6789]\d{9}$',
            message='Phone number must be 10 digits and starts with either(6,7,8,9)',
            code='invalid_number'
        ),
    ])
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    is_active = models.BooleanField(default=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
