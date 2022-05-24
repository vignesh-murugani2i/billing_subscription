from rest_framework import serializers

#from subscription.serializer import SubscriptionSerializer
from subscription.serializer import SubscriptionSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number", "user_name", "password"
                  , "created_at", "updated_at", "is_active", "tenant")


class UserInfoSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number", "user_name", "password"
                  , "created_at", "updated_at", "is_active", "tenant", "subscriptions")
