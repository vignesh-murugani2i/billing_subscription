from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from subscription.models import Subscription
from subscription.serializer import SubscriptionSerializer


@api_view(['POST'])
def create_subscription(request):
    """Creates new subscription"""

    try:
        new_tenant = SubscriptionSerializer(data=request.data)
        new_tenant.is_valid(raise_exception=True)
        new_tenant.save()
        return Response(new_tenant.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
def get_all_subscription(request):
    subscriptions = Subscription.objects.filter(is_active=True)
    if subscriptions.exists():
        subscriptions = SubscriptionSerializer(instance=subscriptions, many=True)
        return Response(subscriptions.data)
    else:
        print("no subscriptions")
        return Response("No subscriptions")
