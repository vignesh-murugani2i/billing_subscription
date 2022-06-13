from django.core.validators import RegexValidator
from django.db import models

# from user.models import User


class Tenant(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, validators=[
        RegexValidator(
            regex='^[A-Za-z0-9@#$%^&+=]{8,}$',
            message='Password length must be 8 or above',
            code='invalid_password'
        ),
    ])
    is_active = models.BooleanField(default=True)
    #created_by = models.ForeignKey(User, default=None)
