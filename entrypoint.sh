#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

# Check DB availability before applying migrations
while ! nc -z $DB_HOST 5432; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is ready!"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn fitnesshub.wsgi:application --bind 0.0.0.0:8000
