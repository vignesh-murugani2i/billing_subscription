from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from plan.models import Plan
from plan.serializer import PlanSerializer
from service.models import Service
from service.serializer import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """This class provides all the CRUD functionalities for Service"""

    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_plans_by_service_id(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        plans = Plan.objects.filter(service_id=service_id)
        plans = PlanSerializer(instance=plans, many=True, )
        return Response(plans.data)
