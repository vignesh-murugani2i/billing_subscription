import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.service import get_all_payments_by_user_id
from subscription.service import get_subscriptions_by_user_id
from user.models import User
from user.serializer import UserSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_user(request):
    """
    Creates a new user with user given details in database.

    :param request: it holds new user details
    :return: It returns newly created user details with user id
    """

    print(("this is logged user"))
    current_user = request.user
    current_user_id = current_user.id

    try:
        request.data["created_by"] = current_user_id
        new_user = UserSerializer(data=request.data)

        new_user.is_valid(raise_exception=True)
        new_user.save()
        logger.debug('New User created with Id: {}'.format(new_user.data['id']))
        return Response(('New User created with Id: {}'.format(new_user.data['id'])))
    except ValidationError as error:
        logger.debug(f'Validation error:{error.message}')
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
def get_all_user(request):
    """
    Gets List of all user from database.

    :param request: for get all user details.
    :return: It returns List of all user.
    """
    fields = ("id", "name", "email", "phone_number", "tenant")

    users = User.objects.all().filter(is_active=True)
    if users.exists():
        user_list = UserSerializer(instance=users, many=True, fields=fields)
        logger.debug("get all user from database")
        return Response(user_list.data)
    else:
        logger.debug("No users found")
        return Response("No users")


@api_view(['GET'])
def get_user_by_id(request, user_id):
    """
    Gets a particular user by user id.

    :param request: for get particular user.
    :param user_id: it holds user id.
    :return: It returns particular user details.
    """
    fields = ("id", "name", "email", "phone_number", "tenant")

    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details = UserSerializer(user_details, fields=fields)
            logger.debug(f"get particular user details of id {user_id}")
            return Response(user_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        logger.debug(f"No user found for this id")
        return Response({'message': 'No such user'})


@api_view(['PUT'])
def update_user_by_id(request, user_id):
    """
    Updates a particular user details by user id.

    :param request: for update particular user
    :param user_id: it holds user id
    :return: returns updated user details.
    """

    try:
        existing_user_data = User.objects.get(pk=user_id)
        updated_user_data = UserSerializer(existing_user_data,
                                           data=request.data, partial=True)
        updated_user_data.is_valid(raise_exception=True)
        updated_user_data.save()
        logger.debug(f"updating particular user detail of id {user_id}")
        return Response(f"successfully updated user detail of id {user_id}")
    except ValidationError as error:
        logger.debug(f"validation error {error.message}")
        return Response({'message': error.message}, status=400)


@api_view(['DELETE'])
def delete_user_by_id(request, user_id):
    """
    Changes a particular user's active status as False in database by user id.

    :param request: for Delete particular user
    :param user_id: it holds user id
    :return: It returns particular user deleted or not
    """

    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details.is_active = False
            user_details.save()
            logger.debug(f"Deactivate user id {user_id}'s active status")
            return Response(f"user id {user_id} is deleted_successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        logger.debug(f"No user found for this id")
        return Response(f"No user found for this id")


@api_view(['GET'])
def get_all_subscription_by_user_id(request, user_id):
    """
    Get all subscriptions of particular user by user id.

    :param request: it holds request params
    :param user_id: it holds user id
    :return: it returns subscription list of particular user
    """

    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details = get_subscriptions_by_user_id(user_id)
            logger.debug(f"get all subscription for user id {user_id}")
            if len(user_details) == 0:
                response = "no subscription found"
            else:
                response = user_details
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f'no user found for this {user_id}')
        response = "no user found"

    return Response(response)


@api_view(['GET'])
def get_payments_by_user_id(request, user_id):
    """
    Get all payments of particular user.

    :param request: It holds all request params
    :param user_id: It holds user id
    :return: It returns all payment list of particular user.
    """

    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            payment_list = get_all_payments_by_user_id(user_id)
            if len(payment_list) > 0:
                logger.debug(f"get all payments for user id {user_id}")
                response = payment_list
            else:
                logger.debug(f"No payment found for user id {user_id}")
                response = "no payment found"
        else:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        logger.debug(f"No user found for user id {user_id}")
        response = "no user found"

    return Response(response)
