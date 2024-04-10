#!/bin/bash
virtual venv && source venv/bin/activate
pip install psycopg2-binary
python manage.py makemigrations && python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('boss', 'admin@example.com', 'boss')" | python manage.py shell
python manage.py collectstatic && gunicorn --workers 2 employee_manage.wsgi