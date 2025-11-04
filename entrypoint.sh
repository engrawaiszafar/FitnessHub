#!/bin/sh

# This script is the "ENTRYPOINT" for the Docker container.

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# exec "$@" runs the command passed to the container,
# which in our case will be Gunicorn.
exec "$@"