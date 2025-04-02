# Builder stage - Alpine for minimal size
FROM python:3.13-alpine AS builder

WORKDIR /app

# Install build dependencies (only what's needed)
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# Only copy what's needed for installation
COPY requirements.txt /app/

# Create virtual environment and install dependencies efficiently
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir --no-compile -r requirements.txt && \
    .venv/bin/pip install --no-cache-dir gunicorn && \
    # Clean up caches and unnecessary files
    find /app/.venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -name "*.pyc" -delete && \
    rm -rf /app/.venv/lib/python*/site-packages/pip && \
    rm -rf /app/.venv/lib/python*/site-packages/setuptools && \
    # Remove build dependencies
    apk del .build-deps

# Final stage - Minimal alpine image
FROM python:3.13-alpine

WORKDIR /app

# Copy only the application code
COPY app.py /app/

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Use an unprivileged user
RUN adduser -D appuser
USER appuser

CMD ["/app/.venv/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
