import smtplib
from datetime import timedelta

from django.core.mail import send_mail
from django.utils.datetime_safe import date

from billing_subscription_api import settings
from subscription.models import Subscription
from subscription.serializer import SubscriptionSerializer


def send_mail_to_subscriber(mail_subject, mail_message, subscriber_mail):
    """
    sends mail to subscriber with some information like subscription ended
    or remind subscription

    :param mail_subject: subject message of mail
    :param mail_message: body message of mail
    :param subscriber_mail: it holds subscriber mail id
    :return:
    """
    is_mail_sent = True
    try:
        send_mail(
            subject=mail_subject,
            message=mail_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber_mail],
        )
        is_mail_sent = True
    except smtplib.SMTPResponseException as mail_error:
        is_mail_sent = False
    return is_mail_sent


def set_next_subscription_date(subscription):
    """
    Sets next subscription date of subscription.

    :param subscription: It holds subscription details
    :return: It returns next subscription date modified object
    """
    end_date = subscription.subscription_end_date

    if date.today() == end_date:
        mail_subject = "Reminder for subscription plan ended"
        mail_message = "Your subscription plan has been expired"
        subscriber_mail = subscription.user.email
        send_mail_to_subscriber(mail_subject, mail_message,
                                subscriber_mail)
        subscription.is_active = False
    else:
        next_subscription_date = subscription.next_subscription_date
        plan_type = int(subscription.plan.plan_type)
        if plan_type == 1:
            next_subscription_date = next_subscription_date + timedelta(days=30)
        elif plan_type == 2:
            next_subscription_date = next_subscription_date + timedelta(days=120)
        elif plan_type == 3:
            next_subscription_date = next_subscription_date + timedelta(days=365)
        subscription.next_subscription_date = next_subscription_date
        subscription.remind_date = subscription.next_subscription_date - timedelta(days=2)
        print(subscription.next_subscription_date)
        subscription.save()
        return subscription


def get_subscriptions_by_user_id(user_id):
    fields = ("id", "tenant", "user", "service", "plan", "start_subscription_date",
              "cycle_count", "next_subscription_date", "subscription_end_date", "remind_date")
    subscriptions = Subscription.objects.filter(user_id=user_id, is_active=True)
    subscriptions = SubscriptionSerializer(instance=subscriptions, many=True, fields=fields)
    return subscriptions.data
