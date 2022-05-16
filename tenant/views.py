from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
    """Gets tenant by id"""

    try:
        tenant_details = Tenant.objects.get(pk=tenant_id)
        if tenant_details.is_active:
            tenant_details = TenantSerializer(tenant_details)
            return Response(tenant_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        return Response("no user found")


@api_view(['GET'])
def get_all_tenant(request):
    """Gets all tenant"""

    tenants = Tenant.objects.filter(is_active=True)
    if tenants is not None:
        tenant_list = TenantSerializer(instance=tenants, many=True)
        return Response(tenant_list.data)
    else:
        print("no tenants")
        return Response("No tenants")


@api_view(['PUT'])
def update_tenant_by_id(request, tenant_id):
    """Updates tenant details by id"""

    try:
        existing_tenant_data = Tenant.objects.get(pk=tenant_id)
        updated_tenant_data = TenantSerializer(existing_tenant_data,
                                               data=request.data, partial=True)
        updated_tenant_data.is_valid(raise_exception=True)
        updated_tenant_data.save()
        return Response(updated_tenant_data.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


@api_view(['DELETE'])
def delete_tenant_by_id(request, tenant_id):
    """Deletes tenant by id"""

    try:
        tenant_details = Tenant.objects.get(pk=tenant_id)
        if tenant_details.is_active:
            tenant_details.is_active = False
            tenant_details.save()
            return Response("tenant deleted successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        return Response("no user found")
