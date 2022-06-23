import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.models import Payment
from payment.serializer import PaymentSerializer
from subscription.models import Subscription
from subscription.serializer import SubscriptionSerializer
from tenant.models import Tenant
from tenant.serializer import TenantSerializer
from user.models import User
from user.serializer import UserSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
@protected_resource(scopes=['superuser'])
def create_tenant(request):
    """
    Creates a new tenant with given details in database.

    :param request: it holds new tenant details
    :return: It returns newly created tenant details with tenant id
    """
    current_user = request.user
    current_user_id = current_user.id

    try:

        request.data["created_by"] = current_user_id
        new_tenant = TenantSerializer(data=request.data)
        new_tenant.is_valid(raise_exception=True)
        new_tenant.save()
        logger.debug('New Tenant created with Id: {}'.format(new_tenant.data['id']))
        return Response('New Tenant created with Id: {}'.format(new_tenant.data['id']))
    except ValidationError as error:
        logger.debug(f'Validation error:{error.message}')
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_tenant_by_id(request, tenant_id):
    """
    Gets a particular details tenant by tenant id.

    :param request: for get particular tenant.
    :param tenant_id: it holds tenant id.
    :return: It returns particular tenant details.
    """
    fields = ("id", "name",)

    try:
        tenant_details = Tenant.objects.get(pk=tenant_id)
        if tenant_details.is_active:
            tenant_details = TenantSerializer(tenant_details, fields=fields)
            logger.debug(f"get particular tenant details of id {tenant_id}")
            return Response(tenant_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f"No user found for this id {error}")
        return Response("no tenant found")


@api_view(['GET'])
@protected_resource(scopes=['superuser'])
def get_all_tenant(request):
    """
    Gets List of all tenant from database.

    :param request: for get all tenant details.
    :return: It returns List of all tenant.
    """

    fields = ("id", "name")
    tenants = Tenant.objects.filter(is_active=True)
    if tenants.exists():
        tenant_list = TenantSerializer(instance=tenants, many=True, fields=fields)
        logger.debug("get all tenant from database")
        return Response(tenant_list.data)
    else:
        logger.debug("No tenants available")
        return Response("No tenants")


@api_view(['PUT'])
@protected_resource(scopes=['admin'])
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
        logger.debug(f"updating particular tenant detail of id {tenant_id}")
        return Response(f"updated particular tenant detail of id {tenant_id}")
    except ValidationError as error:
        logger.debug(f"validation error {error.message}")
        return Response({'message': error.message}, status=400)


@api_view(['DELETE'])
@protected_resource(scopes=['admin'])
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
            logger.debug(f"Deactivate tenant id {tenant_id}'s active status")
            return Response(f"tenant id {tenant_id} deleted successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f"error while deleting tenant id {tenant_id}")
        return Response("no tenant found")


@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_all_user_by_tenant_id(request, tenant_id):
    """
    Gets all users of tenant by tenant id.

    :param request: It holds all request params
    :param tenant_id: It holds tenant id.
    :return: It returns all user list of tenant
    """

    try:
        tenant = Tenant.objects.get(pk=tenant_id)
        if tenant.is_active:
            users = User.objects.filter(tenant_id=tenant_id)
            if len(users) > 0:
                users = UserSerializer(instance=users, many=True, )
                logger.debug(f"get all users of tenant id {tenant_id}")
                return Response(users.data)
            else:
                return Response("no users found")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f"Tenant does not exist or is not active tenant :{error}")
        return Response("no tenant found")


@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_all_subscriptions_by_tenant_id(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
        if tenant.is_active:
            subscriptions = Subscription.objects.filter(tenant_id=tenant_id, is_active=True)
            if len(subscriptions) > 0:
                subscriptions = SubscriptionSerializer(instance=subscriptions, many=True)
                logger.debug(f"get all subscriptions of tenant id {tenant_id}")
                return Response(subscriptions.data)
            else:
                return Response("no subscriptions found")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f"Tenant does not exist or is not active tenant :{error}")
        return Response("no tenant found")


@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_all_payments_by_tenant_id(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
        if tenant.is_active:
            payments = Payment.objects.filter(tenant_id=tenant_id,)
            if len(payments) > 0:
                payments = PaymentSerializer(instance=payments, many=True)
                logger.debug(f"get all subscriptions of tenant id {tenant_id}")
                return Response(payments.data)
            else:
                return Response("no payments found")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist as error:
        logger.debug(f"Tenant does not exist or is not active tenant :{error}")
        return Response("no tenant found")
