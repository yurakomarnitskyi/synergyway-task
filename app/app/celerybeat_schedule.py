from celery.schedules import crontab
from .celery import app

beat_schedule = {
    'fetch-next-user': {
        'task': 'user.tasks.fetch_and_save_next_user',
        'schedule': crontab(minute='*/5'),
    },
}
app.conf.beat_schedule = beat_schedule
