from django.db import models

from user.models import User


class Card(models.Model):
    CARD_CHOICE = (
        ("visa", "visa"),
        ("rupay", "rupay"),
        ("master card", "master card")
    )
    card_type = models.CharField(choices=CARD_CHOICE, max_length=15)
    card_number = models.BigIntegerField()
    cvv_number = models.IntegerField()
    expires_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
