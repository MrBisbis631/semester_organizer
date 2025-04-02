FROM python:3.13-slim as builder

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install dependencies
COPY requirements.txt /app/
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "$(nproc)", "-b", "0.0.0.0:5000", "app:app"]
