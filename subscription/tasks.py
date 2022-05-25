import smtplib

from celery import shared_task
from django.db import transaction


@shared_task(bind=True)
def test_func(self):
    return "Done"

@shared_task(bind=True)
def for_test(self):
    with transaction.atomic():
        print("email working....")
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.starttls()
        mail_server.login("subscriptionforyou45@gmail.com", "just$for$demo")
        mail_server.sendmail("subscriptionforyou45@gmail.com", 'vigneshmurugan290599@gmail.com', "just for fun")
        mail_server.quit()


