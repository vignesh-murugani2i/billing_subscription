from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer, UserInfoSerializer


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
        return Response(new_user.data)
    except ValidationError as error:
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
        return Response(user_list.data)
    else:
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
            return Response(user_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
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
        return Response(updated_user_data.data)
    except ValidationError as error:
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
            return Response(f"user id {user_id} is deleted_successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return Response(f"No user found for this id")


@api_view(['GET'])
def get_all_subscription_by_user_id(request, user_id):
    try:
        user_details = User.objects.get(pk=user_id)
        if user_details.is_active:
            user_details = UserInfoSerializer(user_details)
            return Response(user_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        return Response("no user found")

