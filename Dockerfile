# Use a slim Python base image for building
FROM python:3.13-slim as builder

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y gcc libffi-dev libmagic build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /app/.venv

# Copy dependencies file and install dependencies
COPY requirements.txt .
RUN /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# Final slim image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application files
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PATH="/app/.venv/bin:$PATH"

# Expose port 5000
EXPOSE 5000

# Run Gunicorn with optimal settings
CMD ["/app/.venv/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
