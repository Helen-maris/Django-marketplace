from my_project.celery import app

from django.core.mail import send_mail
from celery.schedules import crontab


@app.task
def send_mail_task(emails):
    send_mail(
        'New ad just published',
        'There is a new ad in Electronics category.',
        'from@example.com',
        emails,
        fail_silently=False,
        )


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=10, minute=30, day_of_week='monday'), weekly_mail_task.s())


@app.task
def weekly_mail_task():
    from main.views import weekly_mail
    curr_week_ads, emails = weekly_mail()
    send_mail(
        'This week\'s ads',
        'New ads: {0}'.format(', '.join(list(curr_week_ads))),
        'from@example.com',
        list(emails),
        fail_silently=False,
    )
