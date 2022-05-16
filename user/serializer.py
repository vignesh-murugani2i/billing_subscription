from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number", "user_name", "password"
                  , "created_at", "updated_at", "is_active", "tenant")
