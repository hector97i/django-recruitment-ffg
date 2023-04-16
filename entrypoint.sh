#!/bin/bash
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn -c config/gunicorn/conf.py --reload --bind :80  image_app.wsgi:application
