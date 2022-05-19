from rest_framework import serializers

from card.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "card_type", "card_number", "cvv_number", "expires_date", "user")
