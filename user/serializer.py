from django.contrib.auth.password_validation import validate_password
from oauth2_provider.models import Application
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
from utils.dynamic_serializer import DynamicFieldsModelSerializer


# def validate_email(value):
#     if User.objects.filter(email=value).exists():
#         raise serializers.ValidationError(f"{value} is already Exist.")


class UserSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number", "password"
                  , "created_at", "updated_at", "is_active", "is_staff", "is_admin",
                  "is_superuser", "created_by", "user_role", "tenant")

    def create(self, validated_data):
        user = User.objects.create(
            # name=validated_data['name'],
            # email=validated_data['email'],
            # phone_number=validated_data['phone_number'],
            # is_staff=validated_data['is_staff'],
            # is_admin=validated_data['is_admin'],
            # is_superuser=validated_data['is_superuser'],
            # created_by=validated_data['created_by'],
            # user_role=validated_data['user_role'],
            # tenant=validated_data['tenant']
            **validated_data
        )

        user.set_password(validated_data['password'])
        user.save()
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name
        )
        application.save()
        print(application)
        return user

    # def update(self, instance, validated_data):(self, validated_data):
    #     user = User.objects.create(
    #         # name=validated_data['name'],
    #         # email=validated_data['email'],
    #         # phone_number=validated_data['phone_number'],
    #         # is_staff=validated_data['is_staff'],
    #         # is_admin=validated_data['is_admin'],
    #         # is_superuser=validated_data['is_superuser'],
    #         # created_by=validated_data['created_by'],
    #         # user_role=validated_data['user_role'],
    #         # tenant=validated_data['tenant']
    #         **validated_data
    #     )
    #
    #     user.set_password(validated_data['password'])
    #     user.save()

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        print("sss")
        instance.set_password(validated_data['password'])
        #user.save()
        instance.save()
        return instance