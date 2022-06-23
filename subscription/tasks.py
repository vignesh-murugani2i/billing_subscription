import smtplib
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
from django.utils.datetime_safe import date
from rest_framework.response import Response

from billing_subscription_api import settings
from subscription.models import Subscription
# from subscription.serializer import SubscriptionInfoSerializer
from subscription.service import send_mail_to_subscriber
from user.models import User

logger = logging.getLogger('root')


@shared_task(bind=True)
def remind_all_subscriptions(self):
    failed_mail_list = []
    success_mail_list = []
    today_date = date.today()
    reminder_list = Subscription.objects.filter(remind_date="2022-06-21", is_active=True)
    mail_subject = "Just For Reminder"
    for subscription_detail in reminder_list:
        plan_amount = subscription_detail.plan.amount
        service_name = subscription_detail.service.name
        subscriber_mail = subscription_detail.user.email
        mail_message = f"your {service_name} subscription for plan {plan_amount} " \
                       f"will be subscribed on {subscription_detail['next_subscription_date']}"

        logger.debug("start to sent mail")
        if send_mail_to_subscriber(mail_subject, mail_message,
                                   subscriber_mail):
            logger.debug("mail sent")
            success_mail_list.append(subscriber_mail)
        else:
            failed_mail_list.append(subscriber_mail)
