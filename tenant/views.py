from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tenant.models import Tenant
from tenant.serializer import TenantSerializer


@api_view(['POST'])
def create_tenant(request):
    """
    Creates a new tenant with given details in database.

    :param request: it holds new tenant details
    :return: It returns newly created tenant details with tenant id
    """

    try:
        new_tenant = TenantSerializer(data=request.data)
        new_tenant.is_valid(raise_exception=True)
        new_tenant.save()
        return Response(new_tenant.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
def get_tenant_by_id(request, tenant_id):
    """
    Gets a particular details tenant by tenant id.

    :param request: for get particular tenant.
    :param tenant_id: it holds tenant id.
    :return: It returns particular tenant details.
    """

    try:
        tenant_details = Tenant.objects.get(pk=tenant_id)
        if tenant_details.is_active:
            tenant_details = TenantSerializer(tenant_details)
            return Response(tenant_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        return Response("no tenant found")


@api_view(['GET'])
def get_all_tenant(request):
    """
    Gets List of all tenant from database.

    :param request: for get all tenant details.
    :return: It returns List of all tenant.
    """

    tenants = Tenant.objects.filter(is_active=True)
    if tenants.exists():
        tenant_list = TenantSerializer(instance=tenants, many=True)
        return Response(tenant_list.data)
    else:
        return Response("No tenants")


@api_view(['PUT'])
def update_tenant_by_id(request, tenant_id):
    """
    Updates a particular tenant details by tenant id.

    :param request: for update particular tenant
    :param tenant_id: it holds tenant id
    :return: returns updated tenant details.
    """

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
    """
    Changes a particular tenant's active status as False in database by tenant id.

    :param request: for Delete particular tenant
    :param tenant_id: it holds tenant id
    :return: It returns particular tenant deleted or not
    """

    try:
        tenant_details = Tenant.objects.get(pk=tenant_id)
        if tenant_details.is_active:
            tenant_details.is_active = False
            tenant_details.save()
            return Response("tenant deleted successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        return Response("no tenant found")
