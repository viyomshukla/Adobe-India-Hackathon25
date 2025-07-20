# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY main_api.py ./
COPY main.py ./
COPY download_models.py ./
COPY download_st_model.py ./

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Set the default command to run the backend
CMD ["python", "main_api.py"] 