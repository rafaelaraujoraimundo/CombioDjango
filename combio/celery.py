from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define a variável de ambiente padrão do Django para o módulo de configurações do projeto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'combio.settings')

app = Celery('combio')

# Carrega as configurações do Celery a partir das configurações do Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks de todos os aplicativos Django instalados.
app.autodiscover_tasks()