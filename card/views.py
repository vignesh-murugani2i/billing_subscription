from datetime import datetime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from card.models import Card
from card.serializer import CardSerializer


@api_view(['POST'])
def create_card(request):
    """
    Creates a new card with user given details in database.

    :param request: it holds new card details
    :return: It returns newly created card details with card id
    """

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


@api_view(['GET'])
def get_card_by_id(request, card_id):
    """
    Gets a particular card details by card id.

    :param request: for get particular card details.
    :param card_id: it holds card id.
    :return: It returns particular card details.
    """

    try:
        card_details = Card.objects.get(pk=card_id)
        if card_details.is_active:
            card_details = CardSerializer(card_details)
            return Response(card_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return Response("no card details found")


@api_view(['GET'])
def get_all_card(request):
    """
    Gets List of all card from database.

    :param request: for get all card details.
    :return: It returns List of all card.
    """

    card_list = Card.objects.filter(is_active=True)
    if card_list:
        card_list = CardSerializer(instance=card_list, many=True)
        return Response(card_list.data)
    else:
        return Response("no card details available")


@api_view(['PUT'])
def update_card_by_id(request, card_id):
    """
    Updates a particular card details by card id.

    :param request: for update particular user
    :param card_id: it holds card id
    :return: returns updated card details.
    """

    try:
        existing_card_details = Card.objects.get(pk=card_id)
        new_card_details = CardSerializer(existing_card_details, data=request.data, partial=True)
        new_card_details.is_valid(raise_exception=True)
        new_card_details.save()
    except ValidationError as error:
        return Response({"message": error.message})


@api_view(['DELETE'])
def delete_card_by_id(request, card_id):
    """
    Changes a particular card's active status as False in database by card id.

    :param request: for Delete particular card
    :param card_id: it holds card id
    :return: It returns particular card deleted or not
    """

    try:
        card_details = Card.objects.get(pk=card_id)
        if card_details.is_active:
            card_details.is_active = False
            card_details.save()
        else:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        return Response("no card details found")
