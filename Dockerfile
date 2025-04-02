# STAGE 1: Build dependencies
FROM python:3.13-slim-bullseye AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for build efficiency
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies only
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    # Try to install constraint package separately
    pip install --no-cache-dir python-constraint && \
    # Install remaining requirements
    grep -v "python-constraint2" requirements.txt > requirements_filtered.txt || true && \
    pip install --no-cache-dir -r requirements_filtered.txt gunicorn

# STAGE 2: Runtime image
FROM python:3.13-slim-bullseye

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Copy only the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy all application code
COPY . .

# Create a non-root user and set ownership
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "app:app"]