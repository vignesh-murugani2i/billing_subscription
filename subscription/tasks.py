import smtplib

from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
from django.utils.datetime_safe import date
from rest_framework.response import Response

from billing_subscription_api import settings
from subscription.models import Subscription
from subscription.serializer import SubscriptionInfoSerializer
from user.models import User


@shared_task(bind=True)
def remind_all_subscriptions(self):
    failed_mail_list = []
    today_date = date.today()
    reminder_list = SubscriptionInfoSerializer(instance=Subscription.objects.filter(
        remind_date__date="2022-05-24"), many=True)
    mail_subject = "Just For Reminder"
    for subscription_detail in reminder_list.data:
        plan_amount = subscription_detail["plan"]['amount']
        service_name = subscription_detail["service"]['name']
        subscriber_mail = User.objects.get(pk=subscription_detail['user']).email
        mail_message = f"your {service_name} subscription for plan {plan_amount} " \
                       f"will be subscribed on {subscription_detail['next_subscription_date'].date()}"
        try:
            send_mail(
                subject=mail_subject,
                message=mail_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber_mail],
                fail_silently=True
            )

        except smtplib.SMTPResponseException as mail_error:
            failed_mail_list.append(subscriber_mail)
