#!/bin/bash
python manage.py collectstatic && python manage.py makemigrations && python manage.py migrate && gunicorn --workers 2 employee_manage.wsgi