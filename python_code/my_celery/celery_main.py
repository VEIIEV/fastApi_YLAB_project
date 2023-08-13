from celery import Celery

from python_code.my_celery.celery_config import celery_settings

celery_app = Celery('excel_worker',
                    include=['python_code.my_celery.tasks'])
celery_app.config_from_object(celery_settings)
celery_app.autodiscover_tasks(['python_code'])

