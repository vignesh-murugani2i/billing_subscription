from django.shortcuts import render

# Create your views here.
import json

import requests
from django.contrib.auth import authenticate
from django.db import models
from oauth2_provider.models import AccessToken, Application
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.constants import SCOPE_OF_SUPERUSER, SCOPE_OF_TENANT_ADMIN, SCOPE_OF_NORMAL_USER


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    print(user)

    if user.is_active:
        app_obj = Application.objects.filter(user=user)

        print(app_obj[0].client_id)
        url = 'http://' + request.get_host() + '/o/token/'
        data_dict = {"grant_type": "password", "username": request.data['username'],
                     "password": request.data['password'], "client_id": app_obj[0].client_id,
                     "scope": give_scopes_based_on_user_role(user)}

        token_obj = requests.post(url=url, data=data_dict)
        token_obj = json.loads(token_obj.text)
        return Response(token_obj)
    else:
        return Response("Invalid user")


def give_scopes_based_on_user_role(user):
    scope = None
    if user.is_active and user.user_role == "super_user":
        scope = SCOPE_OF_SUPERUSER
    elif user.is_active and user.user_role == "tenant_admin":
        scope = SCOPE_OF_TENANT_ADMIN
    elif user.is_active and user.user_role == "subscriber":
        scope = SCOPE_OF_NORMAL_USER
    return scope
