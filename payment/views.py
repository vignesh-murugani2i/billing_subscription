from datetime import timedelta

from django.shortcuts import render
from django.utils.datetime_safe import date, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.models import Payment
from subscription.models import Subscription


@api_view(['POST'])
def make_all_subscriptions_payment(request):
    today_date = date.today()
    today_date = "2022-05-24"
    today_subscription_list = Subscription.objects.filter(is_active=True,
                                                          next_subscription_date__date=today_date
                                                          ).order_by('next_subscription_date')

    if today_subscription_list.exist():
        for subscription in today_subscription_list:
            payment = Payment(
                user=subscription.user,
                tenant=subscription.tenant,
                subscription=subscription,
                amount=subscription.plan.amount,
                payment_date=datetime.today(),
                is_payment_success=True
            )
            payment.save()
            set_next_subscription_date(subscription)
        return Response("Subscription payment done successfully")
    else:
        return Response("There is no subscription today")


def set_next_subscription_date(subscription):
    end_date = subscription.subscription_end_date

    if date.today() == end_date.date():
        subscription.is_active = False
    else:
        next_subscription_date = subscription.next_subscription_date
        plan = subscription.plan
        if plan.plan_type == 1:
            next_subscription_date = next_subscription_date + timedelta(days=30)
        elif plan.plan_type == 2:
            next_subscription_date = next_subscription_date + timedelta(days=120)
        elif plan.plan_type == 3:
            next_subscription_date = next_subscription_date + timedelta(days=365)
        subscription.next_subscription_date = next_subscription_date
        subscription.remind_date = next_subscription_date - timedelta(days=2)
        print(subscription.next_subscription_date)
        subscription.save()

