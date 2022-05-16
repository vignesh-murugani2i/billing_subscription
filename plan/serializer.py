from rest_framework import serializers

from plan.models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "name", "plan_type", "amount", "service")
