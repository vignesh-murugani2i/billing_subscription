from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tenant.models import Tenant
from tenant.serializer import TenantSerializer


@api_view(['POST'])
def create_tenant(request):
    """Creates new tenant"""

    try:
        new_tenant = TenantSerializer(data=request.data)
        new_tenant.is_valid(raise_exception=True)
        new_tenant.save()
        return Response(new_tenant.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
def get_tenant_by_id(request, tenant_id):
    tenant_details = Tenant.objects.get(pk=tenant_id)
    tenant_details = TenantSerializer(tenant_details)
    return Response(tenant_details.data)
