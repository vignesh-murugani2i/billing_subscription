from rest_framework import serializers

from plan.serializer import PlanSerializer
from service.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    #plans = PlanSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ("id", "name", "description")
