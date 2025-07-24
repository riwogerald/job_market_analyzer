import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_analyzer.settings')

app = Celery('job_analyzer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()