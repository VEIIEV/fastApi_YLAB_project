import asyncio
import logging
from datetime import datetime

from python_code.my_celery.celery_main import celery_app
from python_code.utils import read_excel, update_db_from_excel


@celery_app.task
def sync_db_with_excel():

    print('*' * 100)
    loop = asyncio.get_event_loop()

    menus_data, submenus_data, dishes_data = read_excel()
    result = loop.run_until_complete(update_db_from_excel(menus_data, submenus_data, dishes_data))
    print(result)
    print('task complete')

