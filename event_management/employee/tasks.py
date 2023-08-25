from celery import Celery
from celery import shared_task
from celery.schedules import crontab

from .views import send_event_emails

app = Celery('event_management')


@shared_task
def test_task():
    print("This is a test task.")


CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Update this with your broker URL

app.conf.beat_schedule = {
    'send_event_emails': {
        'task': 'employee.tasks.send_event_emails',
        'schedule': crontab(hour=9, minute=0),  # Schedule for 9 AM daily
    },
}
