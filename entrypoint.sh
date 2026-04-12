#!/bin/sh
set -e

# Apply pending database migrations
python manage.py migrate --noinput

# Static files are uploaded to GCS during CI/CD (cloudbuild.yaml), not at boot.
# This keeps container startup fast and avoids GCS credentials at runtime.

# Start Gunicorn bound to the port Cloud Run expects ($PORT, default 8080)
exec gunicorn teamhardball.wsgi:application \
    --bind "0.0.0.0:${PORT:-8080}" \
    --workers 2 \
    --threads 2 \
    --timeout 60 \
    --log-file -
