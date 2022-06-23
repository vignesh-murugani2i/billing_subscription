from __future__ import absolute_import, unicode_literals

import logging
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery.signals import setup_logging
from celery.utils.log import get_task_logger

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billing_subscription_api.settings')
app = Celery('billing_subscription_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace="CELERY")
app.conf.beat_schedule = {
    'trigger_mail_reminder_everyday_at_10_A.M': {
        'task': 'subscription.tasks.remind_all_subscriptions',
        'schedule': crontab(hour=13, minute=21),
    },

    'trigger_subscription_everyday_at_12_A.M': {
        "task": 'payment.tasks.make_all_subscriptions_payment',
        'schedule': crontab(hour=19, minute=18),
    }

}


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
