# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create input, PDF, and output directories
RUN mkdir -p /app/input/PDF /app/output

# Optionally, copy a default input.json if needed (uncomment if you want a default)
# COPY input/input.json /app/input/input.json

# Copy the rest of the backend code
COPY main.py ./
COPY download_models.py ./
COPY download_st_model.py ./

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Set the default command to run the backend
CMD ["python", "main.py"] 