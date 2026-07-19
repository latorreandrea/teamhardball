#!/bin/sh
set -e

# Apply pending database migrations
python manage.py migrate --noinput

# Static files are uploaded to GCS during CI/CD (cloudbuild.yaml), not at boot.
# This keeps container startup fast and avoids GCS credentials at runtime.

# Start Daphne (ASGI server) bound to the port Cloud Run expects ($PORT, default 8080).
# Daphne handles both HTTP and WebSocket traffic — required for the tactical system.
exec daphne \
    --bind "0.0.0.0" \
    --port "${PORT:-8080}" \
    teamhardball.asgi:application