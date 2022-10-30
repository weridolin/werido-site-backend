from core.celery import app
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import zoneinfo

def start_periodic_spider():

    # create schedule
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='*',
        hour='*',
        day_of_week='7',
        day_of_month='*',
        month_of_year='*',
        timezone=zoneinfo.ZoneInfo('Asia/Shanghai')
        )
    