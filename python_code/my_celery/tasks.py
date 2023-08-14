import logging
from datetime import datetime

from python_code.my_celery.celery_main import celery_app


@celery_app.task
def sync_db_with_excel():
    print('*' * 50)
    print('task complete at' + datetime.now().strftime('%H:%M:%S'))
    logging.debug('dsdsdsdsdsds\n')
