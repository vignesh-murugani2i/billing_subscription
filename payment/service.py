import logging

from django.utils.datetime_safe import datetime, date

from payment.models import Payment
from payment.serializer import PaymentSerializer
from subscription.models import Subscription
from subscription.service import send_mail_to_subscriber, set_next_subscription_date

logger = logging.getLogger('root')


def create_payment(subscription_id):
    """
    Created instant payment of new subscription.

    :param subscription_id: It holds subscription id
    :return: It returns new subscription object
    """

    subscription = Subscription.objects.get(pk=subscription_id)
    payment = Payment(
        user=subscription.user,
        tenant=subscription.tenant,
        subscription=subscription,
        amount=subscription.plan.amount,
        payment_date=datetime.today(),
        is_payment_success=True
    )
    payment.save()
    logger.debug(f"instant payment for subscription id {subscription.id}")
    instant_subscription = set_next_subscription_date(subscription)
    return instant_subscription


def get_all_payments_by_user_id(user_id):
    logger.debug(f"getting all payments for user id {user_id}")
    payment_list = Payment.objects.filter(user_id=user_id)
    payment_list = PaymentSerializer(instance=payment_list, many=True)
    return payment_list.data
