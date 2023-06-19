echo "--> Starting beats process"
celery -A dp.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
