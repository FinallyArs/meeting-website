import os
import django
from celery import Celery
from meeting.tasks import SCHEDULE as MEETING_SCHEDULE


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()


app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = MEETING_SCHEDULE

app.autodiscover_tasks()
