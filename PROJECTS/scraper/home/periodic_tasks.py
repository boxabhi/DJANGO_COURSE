from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery.schedules import crontab

schedule, created = IntervalSchedule.objects.get_or_create(
    every=2,  # Every 10 seconds
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.create(
    interval=schedule,
    name='My Periodic Task',
    task='home.tasks.create_news',
)