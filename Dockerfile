# Builder stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Create virtual environment and install dependencies
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt && \
    .venv/bin/pip install --no-cache-dir gunicorn

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Copy application code
COPY . /app/

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

# Add debugging to help identify the issue
RUN ls -la /app && \
    ls -la /app/.venv/bin || echo "venv/bin directory not found"


# Use an unprivileged user
RUN adduser -D appuser
USER appuser

# Use explicit python call to avoid path issues
CMD ["python", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]