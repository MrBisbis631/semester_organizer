# Use a lightweight base image
FROM python:3.13-slim as builder

WORKDIR /app

# Install required system dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies in a virtual environment
COPY requirements.txt /app/
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && .venv/bin/pip install --no-cache-dir gunicorn

# Copy application code
COPY . /app

# Final stage with a minimal runtime image
FROM python:3.13-slim

WORKDIR /app

# Copy the virtual environment and application code from the builder stage
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

# Use gunicorn as the entry point
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
