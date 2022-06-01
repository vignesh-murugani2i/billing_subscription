import logging
from datetime import timedelta

from django.shortcuts import render
from django.utils.datetime_safe import date, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.models import Payment
from subscription.models import Subscription
from subscription.service import set_next_subscription_date

logger = logging.getLogger('root')


@api_view(['POST'])
def make_all_subscriptions_payment(request):
    """
    Makes current date's all subscription payment.

    :param request: It holds request param
    :return: It returns subscription done or no subscription available message
    """
    today_date = date.today()
    today_date = "2022-05-24"
    today_subscription_list = Subscription.objects.filter(is_active=True,
                                                          next_subscription_date__date=today_date
                                                          ).order_by('next_subscription_date')
    logger.debug(f"payment for today subscriptions")
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

        logger.debug(f"all subscription's payment successfully done")
        return Response("Subscription payment done successfully")
    else:
        logger.debug(f"There is no subscription today")
        return Response("There is no subscription today")
