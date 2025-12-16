# Use a slim, lightweight official Python image
FROM python:3.9-slim

# Ensure output is not buffered (good for real-time logging)
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# CRITICAL FIX: Install build dependencies required for psycopg2 to compile
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
# We assume requirements.txt now includes flask, psycopg2-binary, and gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Inform Docker about the exposed port
EXPOSE 5000

# The command that starts the web application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]