from django.utils.datetime_safe import datetime, date

from payment.models import Payment
from payment.serializer import PaymentSerializer
from subscription.models import Subscription
from subscription.service import send_mail_to_subscriber, set_next_subscription_date


def create_payment(subscription_id):
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
    set_next_subscription_date(subscription)
    print("payment done")
    return payment


def get_all_payments_by_user_id(user_id):
    payment_list = Payment.objects.filter(user_id=user_id)
    payment_list = PaymentSerializer(instance=payment_list, many=True)
    return payment_list.data
