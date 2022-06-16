from rest_framework import serializers, request

from plan.serializer import PlanSerializer
from service.serializer import ServiceSerializer
from subscription.models import Subscription
# from user.serializer import UserSerializer
# from user.serializer import UserSerializer
from utils.dynamic_serializer import DynamicFieldsModelSerializer


class SubscriptionSerializer(DynamicFieldsModelSerializer):
    #service = ServiceSerializer(many=False, read_only=True)
    # plan = PlanSerializer(many=False, read_only=True)
    # user = UserSerializer(many=False, read_only=True)

    # plan = serializers.SerializerMethodField()
    # service = serializers.SerializerMethodField()
    #
    # def get_plan(self, obj):
    #     print("4444444")
    #     if self.context.get("request").method == "GET":
    #         return obj.plan.amount
    #     else:
    #         return obj.plan.pk
    #
    # def get_service(self, obj):
    #     print("4444444")
    #     if self.context.get("request").method == "GET":
    #         return obj.service.name
    #     else:
    #         return obj.service

    class Meta:
        model = Subscription
        fields = ("id", "tenant", "user", "service", "plan", "card", "remind_days",
                  "account_mail", "start_subscription_date", "cycle_count",
                  "next_subscription_date", "subscription_end_date", "remind_date")
        # fields = '__all__'

# class SubscriptionInfoSerializer(serializers.ModelSerializer):
#     service = ServiceSerializer(many=False, read_only=True)
#     plan = PlanSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = Subscription
#         fields = ("id", "tenant", "user", "service", "plan", "card", "remind_days", "account_mail",
#                   "start_subscription_date", "cycle_count", "created_at",
#                   "updated_at", "is_active", "next_subscription_date", "subscription_end_date", "remind_date")
