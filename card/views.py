from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from card.models import Card
from card.serializer import CardSerializer


@api_view(['POST'])
def create_card(request):
    try:
        print(request.data)
        expiry_date_string = request.data['expires_date']
        expiry_date = datetime.strptime(expiry_date_string, '%m/%Y')
        request.data['expires_date'] = expiry_date.date()
        new_card_details = CardSerializer(data=request.data)
        new_card_details.is_valid(raise_exception=True)
        new_card_details.save()
        return Response(new_card_details.data)
    except ValidationError as error:
        return Response({"message": error.message})
