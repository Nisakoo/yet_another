import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yet_another.settings")


app = Celery("yet_another")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()