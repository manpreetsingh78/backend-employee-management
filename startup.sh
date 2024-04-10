#!/bin/bash
virtual venv && source venv/bin/activate
pip install psycopg2-binary
python manage.py makemigrations && python manage.py migrate 
python manage.py collectstatic && gunicorn --workers 2 employee_manage.wsgi