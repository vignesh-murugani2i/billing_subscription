import logging
import smtplib
from datetime import datetime, timedelta, date

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
# from django.utils.datetime_safe import datetime
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.service import create_payment
from plan.models import Plan
from service.models import Service
from subscription.models import Subscription
from subscription.serializer import SubscriptionSerializer
from subscription.service import send_mail_to_subscriber
from user.models import User

logger = logging.getLogger('root')


@api_view(['POST'])
@protected_resource(scopes=['user'])
def create_subscription(request):
    """Creates new subscription"""
    current_user = request.user
    # current_user_id = current_user.id
    # print(current_user.tenant.id)
    print(current_user.tenant)
    if current_user.tenant:
        request.data["tenant"] = current_user.tenant.id
        request.data["user"] = current_user.id
    try:
        plan_details = Plan.objects.get(id=request.data['plan'])
        plan_type = int(plan_details.plan_type)
        print(request.data)
        if is_duplicate_subscription(request.data):
            response = Response("subscription already exist on this service")
        else:
            start_date_string = request.data['start_subscription_date']
            next_subscription_date = datetime.strptime(start_date_string, "%Y-%m-%d")
            next_subscription_date = next_subscription_date.date()
            subscription_end_date = calculate_subscription_end_date(
                plan_type, int(request.data['cycle_count']), next_subscription_date)
            request.data['next_subscription_date'] = next_subscription_date
            request.data['subscription_end_date'] = subscription_end_date
            #request.data['remind_date'] = calculate_remind_date(next_subscription_date)
            new_subscription = SubscriptionSerializer(data=request.data, context={'request': request})
            new_subscription.is_valid(raise_exception=True)
            new_subscription.save()
            logger.debug(f"subscription created for {new_subscription.data['id']}")
            if next_subscription_date == date.today():
                logger.debug(f"subscription created for {new_subscription.data['id']}"
                             f" with instant payment ")
                instant_subscription = create_payment(new_subscription.data['id'])
                instant_subscription = SubscriptionSerializer(instant_subscription)
                response = Response(f"payment successfully done for your subscription id "
                                    f"{new_subscription.data['id']}")
            else:
                response = Response(f"subscription successfully created with id "
                                    f"{new_subscription.data['id']}")

    except ValidationError as error:
        logger.debug(f"bad request error {error.message}")
        response = Response({'message': error.message}, status=400)

    return response


@api_view(['GET'])
@protected_resource(scopes=['user'])
def get_subscription_by_id(request, subscription_id):
    fields = ("id", "tenant", "user", "service", "plan", "start_subscription_date",
              "cycle_count", "next_subscription_date", "subscription_end_date", )

    try:
        subscription_details = Subscription.objects.get(pk=subscription_id)
        if subscription_details.is_active:
            subscription_details = SubscriptionSerializer(subscription_details,
                                                          fields=fields, context={'request': request})
            logger.debug(f"get particular subscription for id {subscription_id}")
            return Response(subscription_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        logger.debug(f"no user subscription for this id {subscription_id}")
        return Response("no subscription found")


@api_view(['GET'])
@protected_resource(scopes=['superuser'])
def get_all_subscription(request):
    fields = ("id", "tenant", "user", "service", "plan", "start_subscription_date",
              "cycle_count", "next_subscription_date", "subscription_end_date", )
    subscriptions = Subscription.objects.filter(is_active=True)
    if subscriptions.exists():
        subscriptions = SubscriptionSerializer(instance=subscriptions, many=True, fields=fields)
        logger.debug("Get all subscription")
        return Response(subscriptions.data)
    else:
        logger.debug(f"no subscription available")
        return Response("No subscriptions")


@api_view(['PUT'])
@protected_resource(scopes=['superuser', 'tenant_admin', 'subscriber'])
def update_subscription_by_id(request, subscription_id):
    """Updates new subscription by id"""

    try:
        plan_details = Plan.objects.get(id=request.data['plan'])
        plan_type = int(plan_details.plan_type)
        start_date_string = request.data['start_subscription_date']
        start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
        #  next_subscription_date = calculate_next_subscription_date(plan_type, start_date)
        next_subscription_date = start_date
        subscription_end_date = calculate_subscription_end_date(plan_type,
                                                                int(request.data['cycle_count']),
                                                                start_date)
        request.data['next_subscription_date'] = next_subscription_date.strftime('%Y-%m-%d')
        request.data['subscription_end_date'] = subscription_end_date.strftime('%Y-%m-%d')
        existing_subscription_data = Subscription.objects.get(pk=subscription_id)
        updated_subscription_data = SubscriptionSerializer(existing_subscription_data,
                                                           data=request.data, partial=True)
        # new_subscription = SubscriptionSerializer(data=request.data)
        updated_subscription_data.is_valid(raise_exception=True)
        updated_subscription_data.save()
        logger.debug(f"subscription updated successfully for this id {subscription_id}")
        return Response(f"subscription updated successfully for this id {subscription_id}")
    except ValidationError as error:
        logger.debug(f"error while updating subscription id {subscription_id} :"
                     f"{error.message}")
        return Response({'message': error.message}, status=400)


@api_view(['DELETE'])
@protected_resource(scopes=['user'])
def delete_subscription_by_id(request, subscription_id):
    try:
        subscription_details = Subscription.objects.get(pk=subscription_id)
        if subscription_details.is_active:
            subscription_details.is_active = False
            logger.debug(f"subscription id {subscription_id} is deleted")
            return Response(f"subscription id {subscription_id} is deleted_successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        logger.debug(f"no subscription found for this id {subscription_id} ")
        return Response(f"Subscription not found")


def calculate_subscription_end_date(plan_type, cycle_count, start_date):
    if plan_type == 1:
        subscription_end_date = start_date + timedelta(days=cycle_count * 30)
    elif plan_type == 2:
        subscription_end_date = start_date + timedelta(days=cycle_count * 120)
    elif plan_type == 3:
        subscription_end_date = start_date + timedelta(days=cycle_count * 365)
    return subscription_end_date


def calculate_remind_date(next_subscription_date):
    """
    Calculates reminder_date based on next_subscription_date.

    :param next_subscription_date: next subscription date of user subscribed service
    :return: returns reminder_date
    """
    if next_subscription_date > date.today() + timedelta(days=2):
        remind_date = next_subscription_date - timedelta(days=2)
    else:
        remind_date = next_subscription_date

    return remind_date


@api_view(['GET'])
@protected_resource(scopes=['user'])
def remind_all_subscriptions(request):
    """
    Gets today date's all subscriptions and send mail notification to
    the subscriber mail with service and plan detail message

    :param request: for remind all subscriber
    """
    try:
        # # print("####")
        # # mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        # # print("####")
        # # mail_server.starttls()
        # # mail_server.login("subscriptionforyou45@gmail.com", "just$for$demo")
        # # print("####")
        # # today_date = date.today()
        # # print("dsdsdd")
        # reminder_list = Subscription.objects.filter(
        #     remind_date="2022-06-24")
        # print(len(reminder_list))
        # for subscription_detail in reminder_list:
        #     plan_amount = subscription_detail.plan.amount
        #     service_name = subscription_detail.service.name
        #     subscriber_mail = subscription_detail.user.email
        #     mail_message = f"your {service_name} subscription for plan {plan_amount} " \
        #               f"will be subscribed on {subscription_detail.next_subscription_date}"
        #     # mail_server.sendmail("subscriptionforyou45@gmail.com", subscriber_mail, message)
        #     send_mail_to_subscriber("DSDSSD", mail_message,
        #                             subscriber_mail)
        #
        # return Response("mail sent successfully")
        # mail_server.quit()
        failed_mail_list = []
        success_mail_list = []
        today_date = date.today()
        reminder_list = Subscription.objects.filter(next_subscription_date="2022-06-24", is_active=True)
        mail_subject = "Just For Reminder"
        for subscription_detail in reminder_list:
            print(reminder_list)
            plan_amount = subscription_detail.plan.amount
            service_name = subscription_detail.service.name
            subscriber_mail = subscription_detail.user.email
            mail_message = f"your {service_name} subscription for plan {plan_amount} " \
                           f"will be subscribed on {subscription_detail.next_subscription_date}"

            logger.debug("start to sent mail")
            if send_mail_to_subscriber(mail_subject, mail_message,
                                       subscriber_mail):
                logger.debug("mail sent")
                print("dsddd")
                success_mail_list.append(subscriber_mail)
            else:
                failed_mail_list.append(subscriber_mail)

    except smtplib.SMTPResponseException as mail_error:
        return Response("mail failed to send")


def is_duplicate_subscription(new_subscription_details):
    """
    Checks whether given subscription is already exist or not.

    :param new_subscription_details: It holds new subscription details
    :return: Return whether it is duplicate subscription or not
    """
    # is_subscription_exist = True
    existing_subscription = Subscription.objects.filter(
        user_id=new_subscription_details["user"],
        service_id=new_subscription_details["service"],
        plan_id=new_subscription_details["plan"])
    if len(existing_subscription) > 0:
        is_subscription_exist = True
    else:
        is_subscription_exist = False

    return is_subscription_exist
