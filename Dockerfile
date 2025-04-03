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
    .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && .venv/bin/pip install gunicorn

FROM python:3.13-slim

WORKDIR /app

COPY . /app
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

EXPOSE 5000

CMD ["/app/.venv/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
