echo "--> Starting celery process"
celery -A dp.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
