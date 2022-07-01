import logging
from datetime import datetime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from card.models import Card
from card.serializer import CardSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
@protected_resource(scopes=['user'])
def create_card(request):
    """
    Creates a new card with user given details in database.

    :param request: it holds new card details
    :return: It returns newly created card details with card id
    """
    current_user = request.user
    current_user_id = current_user.id
    request.data["user"] = current_user_id

    try:
        print(request.data)
        expiry_date_string = request.data['expires_date']
        expiry_date = datetime.strptime(expiry_date_string, '%m/%Y')
        request.data['expires_date'] = expiry_date.date()
        new_card_details = CardSerializer(data=request.data)
        new_card_details.is_valid(raise_exception=True)
        new_card_details.save()
        logger.debug(f'new card details created with id {new_card_details.data["id"]}')
        return Response(f'new card details added successfully')
    except ValidationError as error:
        logger.debug(f"validation error : {error.message}")
        return Response({"message": error.message})


@api_view(['GET'])
@protected_resource(scopes=['superuser', 'tenant_admin', 'subscriber'])
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
            logger.debug(f"get card details for card id {card_id}")
            return Response(card_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        logger.debug(f"card details not found for id {card_id} ")
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
        logger.debug(f"Get all card details")
        return Response(card_list.data)
    else:
        logger.debug("no card details found")
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
        logger.debug(f"Updating card details for id {card_id}")
        return Response(f"card id {card_id}'s details successfully updated")
    except ValidationError as error:
        logger.debug(f"validation error while updating card details of id{card_id}")
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
            logger.debug(f"deleting card for id {card_id}")
            card_details.save()
        else:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        logger.debug(f"card details not found")
        return Response("no card details found")
