web: gunicorn run:app
worker: celery -A scheduler.celery worker -l INFO

