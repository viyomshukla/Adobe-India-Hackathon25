# Use AMD64-compatible Python base image
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ ./app/

# Create input/output directories (if not mounted)
RUN mkdir -p /app/input /app/output

# Set environment variables for offline, CPU-only
ENV PYTHONUNBUFFERED=1

# Entry point: process all PDFs in /app/input and write to /app/output
CMD ["python", "app/api.py"]