FROM python:slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Debug: Show what's in requirements.txt
RUN echo "=== Checking requirements.txt ===" && \
    cat requirements.txt && \
    echo "=== Files in current directory ===" && \
    ls -la

# Install build tools and upgrade pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel

# Install dependencies with verbose output
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy the rest of the application
COPY . .

# Install in editable mode
RUN pip install --no-cache-dir -e .

# Train the model (if this fails, the build will stop)
RUN python pipeline/training_pipeline.py

COPY start_services.sh .
RUN chmod +x start_services.sh

EXPOSE 8000 5000
CMD ["/app/start_services.sh"]