from rest_framework import serializers

from tenant.models import Tenant
from user.serializer import UserSerializer
from utils.dynamic_serializer import DynamicFieldsModelSerializer


class TenantSerializer(DynamicFieldsModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = ("id", "name", "username", "password", "is_active","users")


# class TenantInfoSerializer(serializers.ModelSerializer):
#     users = UserSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Tenant
#         fields = ("id", "name", "username", "password", "is_active", "users")
