from datetime import timedelta

from celery import shared_task
from django.utils.datetime_safe import date, datetime

from payment.models import Payment
from subscription.models import Subscription
from subscription.service import send_mail_to_subscriber, set_next_subscription_date


@shared_task(bind=True)
def make_all_subscriptions_payment(self):
    today_date = date.today()
    today_date = "2022-05-24"
    today_subscription_list = Subscription.objects.filter(is_active=True,
                                                          next_subscription_date__date=today_date
                                                          ).order_by('next_subscription_date')
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


