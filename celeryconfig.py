CELERY_RESULT_BACKEND = 'rpc://'
CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost//'
CELERY_IMPORTS = ('tasks',)

