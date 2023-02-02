import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

app = Celery('my_project', include=['main.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


import django
django.setup()


from main.views import weekly_mail

curr_week_ads, emails = weekly_mail()


app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'main.tasks.weekly_mail_tasks',
        'schedule': crontab(hour=13, minute=33, day_of_week=4),
        'args': (list(curr_week_ads), list(emails)),
    },
}
