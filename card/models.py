from django.db import models

from user.models import User


class Card(models.Model):
    CARD_CHOICE = (
        ("visa", "visa"),
        ("rupay", "rupay"),
        ("master card", "master card")
    )
    card_type = models.Choices(choices=CARD_CHOICE, max_length=1)
    card_number = models.BigIntegerField()
    expires_date = models.DateField(input_formats=['%m/%Y'])
    user = models.ForeignKey(User, on_delete=models.CASCADE(), related_name='cards')
