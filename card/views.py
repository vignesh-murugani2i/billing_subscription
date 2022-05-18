from django.shortcuts import render
from rest_framework import viewsets

from card.models import Card
from card.serializer import CardSerializer


class CardView(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objetcs.all()
