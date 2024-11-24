from celery import Celery

app = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'check-and-report-every-30-seconds': {
            'task': 'celery_tasks.check_and_report',
            'schedule': 30.0,
        },
    },
)

import celery_tasks