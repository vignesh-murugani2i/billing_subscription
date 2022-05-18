from rest_framework import serializers

from service.serializer import ServiceSerializer
from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
   # service = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = ("id", "tenant", "user", "service", "plan", "account_mail",
                  "start_subscription_date", "cycle_count", "created_at",
                  "updated_at", "is_active","next_subscription_date","subscription_end_date")
