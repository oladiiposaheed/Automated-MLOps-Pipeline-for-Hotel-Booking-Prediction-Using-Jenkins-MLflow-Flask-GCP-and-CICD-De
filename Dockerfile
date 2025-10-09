# Create python image

# Use the official Python image as the base
FROM python:slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are shown immediately
ENV PYTHONUNBUFFERED=1

# Set/create the working directory inside the container
WORKDIR /app

#Run dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt FIRST to leverage Docker's cache
COPY requirements.txt .

# Copy the rest of the application code
COPY . .

# Copy the requirements file into the container
RUN pip install --no-cache-dir -e .

# Train the model and generate artifacts
RUN python pipeline/training_pipeline.py

# Expose both ports: 8000 for Django and 5000 for Flask development server
EXPOSE 8000 5000

# Use a startup script to run both services
COPY start_services.sh .

RUN chmod +x start_services.sh

CMD [ "./start_services.sh" ]

