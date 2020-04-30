from .settings import DRLZ_URL
import os
from celery import Celery, signature
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy.settings')


class CeleryConfig:
    """
    Celery Configuration
    http://docs.celeryproject.org/en/latest/userguide/configuration.html
    """
    timezone = 'UTC'
    beat_schedule = {
        'chained': {
            'task': 'drugs.tasks.update_drugs',
            'schedule': crontab(hour=1, minute=47),
            'options': {
                'queue': 'default',
                'link': signature('drugs.tasks.update_db',
                                  args=(),
                                  queue='default')
            },
            'args': (DRLZ_URL,)
        }
    }

    # Using Redis broker url
    broker_url = os.environ.get('CELERY_BROKER_URL')

    # Using the RPC protocol to store task state and results.
    result_backend = os.environ.get('CELERY_RESULT_BACKEND')


app = Celery()
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()
