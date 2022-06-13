import json

import requests
from django.contrib.auth import authenticate
from django.db import models
from oauth2_provider.models import AccessToken, Application
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def login_user(request):
#     user = authenticate(username=request.data['username'], password=request.data['password'])
#
#     if user:
#         token_obj = AccessToken.objects.filter(user=user)
#         # print(token_obj)
#         app_obj = Application.objects.filter(user=user)
#
#         print(app_obj[0].client_id)
#         url = 'http://' + request.get_host() + '/o/token/'
#         data_dict = {
#             "grant_type": "password",
#             "username": request.data['username'],
#             "password": request.data['password'],
#             "client_id": app_obj[0].client_id,
#             # "client_secret": app_obj[0].client_secret
#         }
#         token_obj = requests.post(url=url, data=data_dict)
#         token_obj = json.loads(token_obj.text)
#         print(">>>>>>>>>>>", token_obj.keys())
#         return Response(request.user)
#     else:
#         return Response("not ok")
#
#     return Response(token_obj)
