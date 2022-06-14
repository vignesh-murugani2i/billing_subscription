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


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    print(user)

    if user:
        token_obj = AccessToken.objects.filter(user=user)
        # print(token_obj)
        app_obj = Application.objects.filter(user=user)

        print(app_obj[0].client_id)
        url = 'http://' + request.get_host() + '/o/token/'
        data_dict = {
            "grant_type": "password",
            "username": request.data['username'],
            "password": request.data['password'],
            "client_id": app_obj[0].client_id,
            "scope": "read"
        }
        # if user.is_active or not user.is_admin or not user.is_staff or not user.is_superuser:
        #     print("welcome")
        #     data_dict["scope"] = 'read'
        token_obj = requests.post(url=url, data=data_dict)
        token_obj = json.loads(token_obj.text)
        # print(">>>>>>>>>>>", token_obj.keys())
        #return Response("ok")
    else:
        return Response("not ok")

    return Response(token_obj)
