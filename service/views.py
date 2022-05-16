from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.models import Service
from service.serializer import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """This class provides all the CRUD functionalities for Service"""

    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


# @api_view(['POST'])
# def create_service(request):
#     try:
#         service_details = ServiceSerializer(data=request.data)
#         service_details.is_valid(raise_exception=True)
#         service_details.save()
#         return Response(service_details.data)
#     except ValidationError as error:
#         return Response({"message": error.message})
