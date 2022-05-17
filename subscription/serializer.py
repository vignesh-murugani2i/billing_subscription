from rest_framework import serializers

from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "tenant", "user", "service", "plan", "account_mail",
                  "start_subscription_date", "cycle_count", "created_at",
                  "updated_at", "is_active")
