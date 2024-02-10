
import os
from celery import Celery
#Celery allows you to schedule periodic tasks that can run in the background at specified intervals

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mobile_expense_tracker.settings')

app = Celery('Mobile_expense_tracker')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all installed applications
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
