from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from plan.models import Plan
from service.models import Service
from service.serializer import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """This class provides all the CRUD functionalities for Service"""

    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    # @action(detail=False, methods=['get'])
    # def items_not_done(request):
    #     plans = Plan.objects.filter(is_active=True)
    #
    #     return Response(plans)
