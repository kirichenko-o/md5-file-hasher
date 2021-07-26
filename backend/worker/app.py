from celery import Celery
from backend.config import conf

app = Celery(
    broker=conf.get('CELERY_BROKER_CONN_STR'),
    backend=conf.get('CELERY_BACKEND_CONN_STR'),
    include=['backend.worker.tasks']
)
