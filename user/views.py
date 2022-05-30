import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.service import get_all_payments_by_user_id
from user.models import User
from user.serializer import UserSerializer, UserInfoSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_user(request):
    """
    Creates a new user with user given details in database.

    :param request: it holds new user details
    :return: It returns newly created user details with user id
    """

    try:
        new_user = UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        logger.debug('New User created with Id: {}'.format(new_user.data['id']))
        return Response(new_user.data)
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

    users = User.objects.all().filter(is_active=True)
    if users.exists():
        user_list = UserSerializer(instance=users, many=True)
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

    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details = UserSerializer(user_details)
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
        return Response(updated_user_data.data)
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
    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details = UserInfoSerializer(user_details)
            logger.debug(f"get all subscription for user id {user_id}")
            return Response(user_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f'no user found for this {user_id}')
        return Response("no user found")


@api_view(['GET'])
def get_payments_by_user_id(request, user_id):
    try:
        user_details = User.objects.get(pk=user_id)
        payment_list = get_all_payments_by_user_id(user_id)
        if user_details.is_active:
            print(len(payment_list))
            if payment_list:
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
