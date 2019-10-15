from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoweb.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
django.setup()

app = Celery('djangoweb')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)