import smtplib
from datetime import datetime, timedelta, date

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
# from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from plan.models import Plan
from service.models import Service
from subscription.models import Subscription
from subscription.serializer import SubscriptionSerializer, SubscriptionInfoSerializer
from user.models import User


@api_view(['POST'])
def create_subscription(request):
    """Creates new subscription"""
    try:
        plan_details = Plan.objects.get(id=request.data['plan'])
        plan_type = int(plan_details.plan_type)
        if request.data.get('start_subscription_date'):
            start_date_string = request.data['start_subscription_date']
            start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
            next_subscription_date = start_date
        else:
            next_subscription_date = datetime.now()

        subscription_end_date = calculate_subscription_end_date(
            plan_type, int(request.data['cycle_count']), next_subscription_date)
        request.data['next_subscription_date'] = next_subscription_date
        request.data['subscription_end_date'] = subscription_end_date
        request.data['remind_date'] = calculate_remind_date(next_subscription_date)
        if is_duplicate_subscription(request.data):
            response = Response("subscription already exist on this service")
        else:
            new_subscription = SubscriptionSerializer(data=request.data)
            new_subscription.is_valid(raise_exception=True)
            new_subscription.save()
            response = Response(new_subscription.data)
    except ValidationError as error:
        response = Response({'message': error.message}, status=400)

    return response


@api_view(['GET'])
def get_subscription_by_id(request, subscription_id):
    try:
        subscription_details = Subscription.objects.get(pk=subscription_id)
        if subscription_details.is_active:
            subscription_details = SubscriptionSerializer(subscription_details)
            return Response(subscription_details.data)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return Response("no user found")


@api_view(['GET'])
def get_all_subscription(request):
    subscriptions = Subscription.objects.filter(is_active=True)
    if subscriptions.exists():
        subscriptions = SubscriptionSerializer(instance=subscriptions, many=True)
        return Response(subscriptions.data)
    else:
        print("no subscriptions")
        return Response("No subscriptions")


@api_view(['PUT'])
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
        return Response(updated_subscription_data.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


def delete_subscription_by_id(request, subscription_id):
    try:
        subscription_details = Subscription.objects.get(pk=subscription_id)
        if subscription_details.is_active:
            subscription_details.is_active = False
            return Response(f"subscription id {subscription_id} is deleted_successfully")
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
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
    if next_subscription_date.date() > date.today() + timedelta(days=2):
        remind_date = next_subscription_date - timedelta(days=2)
    else:
        remind_date = next_subscription_date

    return remind_date.strftime('%Y-%m-%d')


@api_view(['GET'])
def remind_all_subscriptions(request):
    """
    Gets today date's all subscriptions and send mail notification to
    the subscriber mail with service and plan detail message

    :param request: for remind all subscriber
    """
    try:
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.starttls()
        mail_server.login("subscriptionforyou45@gmail.com", "just$for$demo")
        today_date = date.today()
        reminder_list = SubscriptionInfoSerializer(instance=Subscription.objects.filter(
            remind_date="2022-05-20"), many=True)
        for subscription_detail in reminder_list.data:
            plan_amount = subscription_detail["plan"]['amount']
            service_name = subscription_detail["service"]['name']
            subscriber_mail = User.objects.get(pk=subscription_detail['user']).email
            message = f"your {service_name} subscription for plan {plan_amount} " \
                      f"will be subscribed on {subscription_detail['next_subscription_date']}"
            mail_server.sendmail("subscriptionforyou45@gmail.com", subscriber_mail, message)

        return Response("mail sent successfully")
        mail_server.quit()
    except smtplib.SMTPResponseException as mail_error:
        return Response("mail failed to send")


def is_duplicate_subscription(new_subscription_details):
    print(new_subscription_details)
    is_subscription_exist = True
    existing_subscription = Subscription.objects.filter(
        user_id=new_subscription_details["user"],
        service_id=new_subscription_details["service"],
        plan_id=new_subscription_details["plan"])
    if len(existing_subscription) > 0:
        is_subscription_exist = True
    else:
        is_subscription_exist = False

    return is_subscription_exist

# @api_view(['GET'])
# def test(request):
#     test_func.delay()
#     return Response("done")
