from django.core.mail import send_mail
from celery import shared_task
from main.send_sms import send_sms


@shared_task
def send_mail_task(emails):
    send_mail(
        'New ad just published',
        'There is a new ad in Electronics category.',
        'from@example.com',
        emails,
        fail_silently=False,
        )


@shared_task()
def weekly_mail_tasks(curr_week_ads, emails):
    send_mail(
        'This week\'s ads',
        'New ads: {0}'.format(', '.join(list(curr_week_ads))),
        'from@example.com',
        list(emails),
        fail_silently=False,
    )


@shared_task()
def generate_code_task(args):
    code, phone = args
    send_sms(code, phone)
