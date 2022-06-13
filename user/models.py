from django.core.validators import RegexValidator
from django.db import models

from tenant.models import Tenant
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from oauth2_provider.models import AbstractApplication, Application


# class User(models.Model):
#     name = models.CharField(max_length=250, validators=[
#         RegexValidator(
#             regex='^([A-Za-z]{3,})( [a-z]+)*( [a-z]+)*$',
#             message='Please enter valid name',
#             code='invalid_name'
#         ),
#     ])
#     email = models.EmailField(unique=True)
#     phone_number = models.BigIntegerField(validators=[
#         RegexValidator(
#             regex='^[6789]\d{9}$',
#             message='Phone number must be 10 digits and starts with either(6,7,8,9)',
#             code='invalid_number'
#         ),
#     ], unique=True)
#     # user_name = models.CharField(max_length=200)
#     # ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$
#     password = models.CharField(max_length=200, validators=[
#         RegexValidator(
#             regex='^[A-Za-z0-9@#$%^&+=]{8,}$',
#             message='Password length must be 8 or above',
#             code='invalid_password'
#         ),
#     ])
#     created_at = models.DateTimeField(auto_now_add=True, )
#     updated_at = models.DateTimeField(auto_now=True, )
#     is_active = models.BooleanField(default=True)
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
class MyUserManager(BaseUserManager):
    def create_user(self, name, phone_number, email, user_role, password=None):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            user_role=user_role)
        user.set_password(password)
        user.save(using=self._db)
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name
        )
        application.save()
        return user

    def create_superuser(self, name, phone_number, email, user_role, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name=name, phone_number=phone_number,
                                email=email, password=password, user_role=user_role)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ("super_user", "super_user"),
        ("client", "client"),
        ("subscriber", "subscriber"),
    ]

    name = models.CharField(max_length=250, validators=[
        RegexValidator(
            regex='^([A-Za-z]{3,})( [a-z]+)*( [a-z]+)*$',
            message='Please enter valid name',
            code='invalid_name'
        ),
    ])
    email = models.EmailField(unique=True)
    phone_number = models.BigIntegerField(validators=[
        RegexValidator(
            regex='^[6789]\d{9}$',
            message='Phone number must be 10 digits and starts with either(6,7,8,9)',
            code='invalid_number'
        ),
    ], unique=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    is_active = models.BooleanField(default=True)

    # tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users",blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    created_by = models.IntegerField(default=None, null=True)
    user_role = models.CharField(choices=ROLE_CHOICES, max_length=15)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'user_role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
