import time
from datetime import timedelta, datetime

from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task, app
from django.template.loader import get_template

from meeting.models import Profile, Message
from website import settings

@shared_task
def new_messages_email():
    new_messages_ids = set(Profile.objects.filter(
        created_at__gte=datetime.now() - timedelta(
            days=settings.NEW_MESSAGES_DAYS)
    ).values_list('id', flat=True))
    if new_messages_ids:
        send_user_email.delay(list(new_messages_ids))


@shared_task
def send_user_email(user_id, product_ids):
    user = Profile.objects.get(id=user_id)
    messages = Message.objects.all()
    template = get_template('email.html')



    email_message = ''
    for message in messages:
        email_message += f'{message}'
    send_mail(
        subject='New messages',
        message=email_message,
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[user.email],
        html_message=template.render(context={
        'user': user,
        'messages': messages
    })

    )


SCHEDULE = {

    'new_messages_email': {
        'task': 'meeting.tasks.new_messages_email',
        'args': (),
        'options': {},
        # 'schedule': crontab(day_of_week='mon', hour=9, minute=0),
        'schedule': timedelta(seconds=5),
    }
}



