from celery import Celery
from elasticsearch import Elasticsearch


celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task
def ingest_log(log_data):

    es = Elasticsearch("http://localhost:9200")
    print(f'Log ingested: {log_data}')
    es.index(index='logs', body=log_data)
    return 'Log ingested successfully!'
