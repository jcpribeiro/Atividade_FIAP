#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py makemigrations --merge
python manage.py migrate --noinput
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
python manage.py runserver 0.0.0.0:8000
