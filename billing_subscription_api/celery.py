from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
from subscription.tasks import for_test

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billing_subscription_api.settings')
app = Celery('billing_subscription_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.conf.enable_utc = False
app.conf.update(timezone='Asis/Kolkata')
app.config_from_object(settings, namespace="CELERY")
app.conf.beat_schedule = {
    'trigger_mail_reminder_everyday_at_10_P.M': {
        'task': 'subscription.tasks.for_test',
        'schedule': crontab(minute='*/2'),
    }

}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    #or_test