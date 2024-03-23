from django.contrib.admin.models import LogEntry
from celery.schedules import crontab
from django.contrib import admin

from utils import admin

@periodic_task(run_every=crontab(minute='5', hour='*'))
def my_periodic_task():
    # ... código da tarefa periódica ...

# Registrar a tarefa no Django Admin
admin.site.register(LogEntry)