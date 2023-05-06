#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
cd /app/                          # making sure we are in the application folder
python3 manage.py migrate         # migrate existing migrations
python3 manage.py makemigrations  # makes package migrations if needed
python3 manage.py migrate         # migrate package migrations

# collect static files
python3 manage.py collectstatic --noinput

# Start server with gunicorn workers
echo "Starting server"
gunicorn --bind :8000 --workers 3 medical_rec.wsgi:application
