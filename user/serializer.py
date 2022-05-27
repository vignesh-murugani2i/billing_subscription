from rest_framework import serializers

# from subscription.serializer import SubscriptionSerializer
from rest_framework.validators import UniqueValidator

from subscription.serializer import SubscriptionSerializer
from user.models import User


# def validate_email(self, value):
#     lower_email = value.lower()
#     if User.objects.filter(email__iexact=lower_email).exists():
#         raise serializers.ValidationError("Duplicate")
#     return lower_email
def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError(f"{value} is already Exist.")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])

    # email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
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
