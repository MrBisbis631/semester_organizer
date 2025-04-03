# Use a lightweight Python base image
FROM python:3.13-alpine as builder

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create a virtual environment
RUN python -m venv /app/.venv

# Copy dependencies file and install dependencies
COPY requirements.txt .
RUN . /app/.venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Final lightweight image
FROM python:3.13-alpine

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
CMD [".venv/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
