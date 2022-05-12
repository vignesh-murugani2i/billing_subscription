from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer


@api_view(['POST'])
def create_user(request):
    new_user = UserSerializer(data=request.data)
    new_user.is_valid(raise_exception=True)
    new_user.save()
    return Response(new_user.data)


@api_view(['GET'])
def get_all_user(request):
    """Returns a list of all users."""

    # paginator = Paginator(UserDetails.objects.all().filter(is_active=True), 20)
    # users = paginator.get_page(1)
    users = User.objects.all()
    user_list = UserSerializer(instance=users, many=True)
    return Response(user_list.data)


@api_view(['GET'])
def get_user_by_id(request, user_id):
    user_details = User.objects.get(pk=user_id)
    user_details = UserSerializer(user_details)
    return Response(user_details.data)


@api_view(['PUT'])
def update_user_by_id(request, user_id):
    existing_user_data = User.objects.get(pk=user_id)
    updated_user_data = UserSerializer(existing_user_data,
                                       data=request.data, partial=True)
    updated_user_data.is_valid(raise_exception=True)
    updated_user_data.save()
    return Response(updated_user_data.data)


@api_view(['DELETE'])
def delete_user_by_id(request, user_id):
    user_details = User.objects.get(pk=user_id)
    user_details.is_active = False
    user_details.save()
    return Response(f"user id {user_id} is deleted_successfully")
