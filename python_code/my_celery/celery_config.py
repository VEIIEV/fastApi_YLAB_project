from datetime import timedelta


# todo добавить в .env файл rabbitmq
class Config:
    broker_connection_retry_on_startup = True
    broker_url = 'amqp://guest:guest@rabbitmq:5672//'
    result_backend = 'rpc://'
    result_persistent = False
    # imports = ('python_code.my_celery.tasks',)
    timezone = 'Europe/Moscow'
    # настройка расписания
    beat_schedule = {
        'update_db_every_15_seconds': {
            'task': 'python_code.my_celery.tasks.sync_db_with_excel',
            #  'schedule': crontab(minute='*/4')
            'schedule': timedelta(seconds=15)
        },
        # 'update_db_every_15': {
        #     'task': 'sync_db_with_excel',
        #     #  'schedule': crontab(minute='*/4')
        #     'schedule': timedelta(seconds=15)
        # },
    }


celery_settings = Config()
