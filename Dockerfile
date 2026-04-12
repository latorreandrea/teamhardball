# ---- builder: installs Python dependencies ----
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 # Strip tests, dist-info and bytecode to shrink the layer
 && find /usr/local/lib/python3.12/site-packages -type d -name "tests"    -exec rm -rf {} + 2>/dev/null || true \
 && find /usr/local/lib/python3.12/site-packages -type d -name "test"     -exec rm -rf {} + 2>/dev/null || true \
 && find /usr/local/lib/python3.12/site-packages -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true \
 && find /usr/local/lib/python3.12/site-packages -name "__pycache__"      -exec rm -rf {} + 2>/dev/null || true \
 && find /usr/local/lib/python3.12/site-packages -name "*.pyc"            -delete 2>/dev/null || true

# ---- runtime: minimal alpine image ----
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Non-root user
RUN addgroup -S django && adduser -S -G django django

WORKDIR /app

# Copy only the cleaned site-packages and gunicorn binary
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy app source — static/ is excluded via .dockerignore (served from GCS)
COPY --chown=django:django . .

# Clean any residual bytecode from app source
RUN find /app -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
 && find /app -name "*.pyc" -delete 2>/dev/null || true

COPY --chown=django:django entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER django

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
