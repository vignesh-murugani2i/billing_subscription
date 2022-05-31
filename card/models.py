from django.db import models

from user.models import User


class Card(models.Model):
    """This class provides model for card"""

    CARD_CHOICE = (
        (1, "visa"),
        (2, "rupay"),
        (3, "master card")
    )
    card_type = models.CharField(choices=CARD_CHOICE, max_length=15)
    card_number = models.CharField(max_length=256, null=False)
    cvv_number = models.IntegerField()
    expires_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    is_active = models.BooleanField(default=True)
