#!/bin/bash
python src/manage.py migrate
python src/manage.py collectstatic --noinput
gunicorn -c config/gunicorn/conf.py --bind :8000 --chdir src ecg_auto.asgi:application
