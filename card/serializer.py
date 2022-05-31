from rest_framework import serializers

from card.models import Card
from utils.encryption_decryption import encrypt, generate_key


# def get_card_number(card_details):
#     print(card_details)
#     encrypted_card_number = card_details.card_number
#     salt_value = generate_key()
#     encrypted_card_number = encrypt(encrypted_card_number, salt_value)
#     return encrypted_card_number


class CardSerializer(serializers.ModelSerializer):

    # def get_card_number(self, card_details):
    #     print(card_details)
    #     encrypted_card_number = card_details.card_number
    #     salt_value = generate_key()
    #     encrypted_card_number = encrypt(encrypted_card_number, salt_value)
    #     return encrypted_card_number

    class Meta:
        model = Card
        fields = ("id", "card_type", "card_number", "cvv_number", "expires_date", "user")

    def create(self, validated_data):
        salt_value = generate_key()
        validated_data['card_number'] = encrypt(validated_data['card_number'], salt_value)
        card = Card.objects.create(**validated_data)
        return card

