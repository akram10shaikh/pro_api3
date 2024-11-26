#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install gunicorn
pip install git+https://github.com/benoitc/gunicorn.git
pip install -U git+https://github.com/benoitc/gunicorn.git
pip install greenlet
pip install eventlet
pip install gunicorn[eventlet]
pip install gevent
pip install gunicorn[gevent]

pip install -r requirements.txt



python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi