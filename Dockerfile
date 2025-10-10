# Create python image

# Use the official Python image as the base
FROM python:slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

# Set/create the working directory inside the container
WORKDIR /app

#Run dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all the requirements file and install dependencies into the container

COPY . .

# Install build tools
RUN pip install --no-cache-dir setuptools wheel

# Install dependencies from requirements.txt FIRST
RUN pip install --no-cache-dir -r requirements.txt

# THEN install the package in editable mode
RUN pip install --no-cache-dir -e .

# Train the model and generate artifacts
RUN python pipeline/training_pipeline.py

# Copy the startup script
COPY start_services.sh .

# Make the script executable (Linux container needs this)
RUN chmod +x start_services.sh

# Expose both ports: 8000 for Django and 5000 for Flask development server
EXPOSE 8000 5000

CMD ["/app/start_services.sh"]