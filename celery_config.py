# celery_config.py
from celery import Celery
import celery

celery_app = Celery('generate')

# Configure Celery to use Redis as the broker
celery_app.conf.update(
    broker_url='redis://localhost:6379/0',
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True ,
)

# Other Celery configurations can go here
