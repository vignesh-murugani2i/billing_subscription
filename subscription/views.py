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
from subscription.serializer import SubscriptionSerializer
from user.models import User


@api_view(['POST'])
def create_subscription(request):
    """Creates new subscription"""
    try:
        plan_details = Plan.objects.get(id=request.data['plan'])
        plan_type = int(plan_details.plan_type)
        start_date_string = request.data['start_subscription_date']
        start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
        next_subscription_date = start_date
        subscription_end_date = calculate_subscription_end_date(
            plan_type, int(request.data['cycle_count']), start_date)
        request.data['next_subscription_date'] = next_subscription_date.strftime('%Y-%m-%d')
        request.data['subscription_end_date'] = subscription_end_date.strftime('%Y-%m-%d')
        request.data['remind_date'] = calculate_remind_date(next_subscription_date)
        new_subscription = SubscriptionSerializer(data=request.data)
        new_subscription.is_valid(raise_exception=True)
        new_subscription.save()
        return Response(new_subscription.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


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


# def calculate_next_subscription_date(plan_type, start_date):
#
#     if start_date.date() == date.today():
#         next_subscription_date = date.today()
#     elif date.today() < start_date.date():
#         next_subscription_date = start_date.date()
#     # elif plan_type == 1:
#     #     next_subscription_date = start_date + timedelta(days=30)
#     # elif plan_type == 2:
#     #     next_subscription_date = start_date + timedelta(days=120)
#     # elif plan_type == 3:
#     #     next_subscription_date = start_date + timedelta(days=365)
#     return next_subscription_date


def calculate_subscription_end_date(plan_type, cycle_count, start_date):
    if plan_type == 1:
        subscription_end_date = start_date + timedelta(days=cycle_count * 30)
    elif plan_type == 2:
        subscription_end_date = start_date + timedelta(days=cycle_count * 120)
    elif plan_type == 3:
        subscription_end_date = start_date + timedelta(days=cycle_count * 365)
    return subscription_end_date


def calculate_remind_date(next_subscription_date):
    # next_subscription_date = subscription_details['next_subscription_date']
    if next_subscription_date.date() > date.today() + timedelta(days=2):
        reminder_list = Subscription.objects.filter(remind_date='2022-05-23').values('user_id', 'plan_id')
        print(reminder_list)
        for i in reminder_list:
            print(i)
        remind_date = next_subscription_date - timedelta(days=2)
    else:
        remind_date = next_subscription_date
    print(remind_date.strftime('%Y-%m-%d'))
    return remind_date.strftime('%Y-%m-%d')


@api_view(['GET'])
def remind_all_subscriptions(request):
    today_date = date.today()

    reminder_list = Subscription.objects.filter(
        remind_date="2022-05-23").values('user_id', 'plan_id', 'service_id', 'next_subscription_date')
    print(reminder_list)
    if reminder_list:
        for subscription_detail in reminder_list:
            plan_details = Plan.objects.get(id=subscription_detail['plan_id'])
            service_details = Service.objects.get(id=subscription_detail['service_id'])
            user_details = User.objects.get(id=subscription_detail['user_id'])
            message = f"your {service_details.name} subscription for plan {plan_details.amount} " \
                      f"will be subscribed on {subscription_detail['next_subscription_date']}"
            subscriber_mail = user_details.email
            send_mail_to_subscriber(message, subscriber_mail)

        return Response("mail sent successfully")
    else:
        return Response("no reminders today")


def send_mail_to_subscriber(message, subscriber_mail):
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    # Authentication
    mail_server.login("subscriptionforyou45@gmail.com", "just$for$demo")
    # message to be sent
    mail_server.sendmail("subscriptionforyou45@gmail.com", subscriber_mail, message)
    print("mail sent")
    # terminating the session
    mail_server.quit()
