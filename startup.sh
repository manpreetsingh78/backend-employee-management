#!/bin/bash
sudo yum -y update
sudo tee /etc/yum.repos.d/pgdg.repo<<EOF
[pgdg12]
name=PostgreSQL 12 for RHEL/CentOS 7 - x86_64
baseurl=https://download.postgresql.org/pub/repos/yum/12/redhat/rhel-7-x86_64
enabled=1
gpgcheck=0
EOF
sudo yum makecache
sudo yum install postgresql12 postgresql12-server
sudo /usr/pgsql-12/bin/postgresql-12-setup initdb
sudo systemctl enable --now postgresql-12
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-12.service to /usr/lib/systemd/system/postgresql-12.service.
sudo -u postgres psql && CREATE DATABASE employee;Alter USER postgres WITH PASSWORD 'admin123';ALTER ROLE postgres SET client_encoding TO 'utf8';ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';ALTER ROLE postgres SET timezone TO 'UTC';GRANT ALL PRIVILEGES ON DATABASE employee TO postgres;exit;
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic && gunicorn --workers 2 employee_manage.wsgi