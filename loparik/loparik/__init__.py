# Это позволит убедиться, что приложение всегда импортируется, когда запускается Django
from .celery import app as celery_app
